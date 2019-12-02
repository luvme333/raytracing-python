#version 430
/*************************************************** DATA STRUCTURES **************************************************/

struct SCamera
{
    vec3 Position;
    vec3 View;
    vec3 Up;
    vec3 Side;
    vec2 Scale;
};

struct SLight
{
    vec3 Position;
};

struct SRay
{
    vec3 Origin;
    vec3 Direction;
};

struct STracingRay
{
	SRay ray;
	float contribution;
	int depth;
};

struct SIntersection
{
    float Time;
    vec3 Point;
    vec3 Normal;
    vec3 Color;
	// ambient, diffuse and specular coeffs
    vec4 LightCoeffs;
    // 0 - non-reflection, 1 - mirror
	float ReflectionCoef;
	float RefractionCoef;
    int MaterialType;
};

struct SSphere
{
    vec3 Center;
    float Radius;
};

struct STriangle
{
    vec3 v1;
    vec3 v2;
    vec3 v3;
    int MaterialIdx;
};

/* CONFIG CONSTANTS **************************************************/

// Ratio of refraction indices of air and glass
const float RefractionIndex = 0.3;
const vec3 RED = vec3 ( 1.0, 0.0, 0.0 );
const vec3 GREEN = vec3 ( 0.0, 1.0, 0.0 );
const vec3 BLUE = vec3 ( 0.0, 0.0, 1.0 );
const vec3 YELLOW = vec3 ( 1.0, 1.0, 0.0 );
const vec3 WHITE = vec3 ( 1.0, 1.0, 1.0 );
const vec3 Zero = vec3 ( 0.0, 0.0, 0.0 );
const vec3 Unit = vec3 ( 1.0, 1.0, 1.0 );
const vec3 AxisX = vec3 ( 1.0, 0.0, 0.0 );
const vec3 AxisY = vec3 ( 0.0, 1.0, 0.0 );
const vec3 AxisZ = vec3 ( 0.0, 0.0, 1.0 );
const vec3 MirrorX = vec3 ( -1.0, 1.0, 1.0 );
const vec3 MirrorY = vec3 ( 1.0, -1.0, 1.0 );
const vec3 MirrorZ = vec3 ( 1.0, 1.0, -1.0 );
const int DIFFUSE_REFLECTION = 1;
const int MIRROR_REFLECTION = 2;
const int REFRACTION = 3;

#define BIG 1000000.0
#define EPSILON 0.001 

/* SHADER INTERFACE **************************************************/
out vec4 FragColor;
in vec3 glPosition;
uniform SCamera uCamera;
uniform SLight uLight;
layout (binding = 2, rgba32f) uniform  imageBuffer uPoints;
layout (binding = 3, rgba32f) uniform  imageBuffer uIndexes;
layout (binding = 4, rgba32f) uniform  imageBuffer uSpheres;

struct SMaterial
{
	//diffuse color
    vec3 Color;
    // ambient, diffuse and specular coeffs
	vec4 LightCoeffs;
    // 0 - non-reflection, 1 - mirror
	float ReflectionCoef;
	float RefractionCoef;
    int MaterialType;
};

uniform SMaterial uMaterials[7];

/*********************************************** INTERSECTION FUNCTIONS ***********************************************/

bool solveQuadratic(const float a, const float b, const float c, out float x0, out float x1)
{
    float discr = b * b - 4 * a * c;
    if (discr < 0) 
		return false;
    else if (discr == 0) 
	{
        x0 = x1 = - 0.5 * b / a;
    }
	else 
	{
        float q = (b > 0) ?
		-0.5 * (b + sqrt(discr)) :
		-0.5 * (b - sqrt(discr));
        x0 = q / a;
        x1 = c / q;
    }
	return true;
}
 

bool IntersectSphere ( SSphere sphere, SRay ray, float start, float final, out float time )
{
    ray.Origin -= sphere.Center;
 /*   float A = dot ( ray.Direction, ray.Direction );
    float B = dot ( ray.Direction, ray.Origin );
    float C = dot ( ray.Origin, ray.Origin ) - sphere.Radius * sphere.Radius;
    float D = B * B - A * C;
    if ( D > 0.0 )
	{
        D = sqrt ( D );
        time = min ( max ( 0.0, ( -B - D ) / A ), ( -B + D ) / A );
        return ( time >= start ) && ( time <= final );
	}
	return false;
	*/
	 float A = dot ( ray.Direction, ray.Direction );
    float B = dot ( ray.Direction, ray.Origin );
    float C = dot ( ray.Origin, ray.Origin ) - sphere.Radius * sphere.Radius;
    float D = B * B - A * C;
    if ( D > 0.0 )
    {
        D = sqrt ( D );
        float t1 = ( -B - D ) / A;
        float t2 = ( -B + D ) / A;
        if(t1 < 0 && t2 < 0)
            return false;
        if(min(t1, t2) < 0)
        {
            time = max(t1,t2);
            return true;
        }
        time = min(t1, t2);
        return true;
    }
    return false;
}


bool RayTriangleIntersection(SRay ray, vec3 v1, vec3 v2, vec3 v3, out float time )
{
    // // Compute the intersection of ray with a triangle using geometric solution 
	// Input: // points v0, v1, v2 are the triangle's vertices 
	// rayOrig and rayDir are the ray's origin (point) and the ray's direction 
	// Return: // return true is the ray intersects the triangle, false otherwise 
	// bool intersectTriangle(point v0, point v1, point v2, point rayOrig, vector rayDir) { 
	// compute plane's normal vector 
	time = -1;
    vec3 A = v2 - v1;
    vec3 B = v3 - v1;
    // no need to normalize vector 
	vec3 N = cross(A, B);
    // N 
	// // Step 1: finding P 
	// // check if ray and plane are parallel ? 
	float NdotRayDirection = dot(N, ray.Direction);
    if ((NdotRayDirection > -EPSILON) && (NdotRayDirection < EPSILON)) 
		return false;
    // they are parallel so they don't intersect ! 
	// compute d parameter using equation 2 
	float d = dot(N, v1);
    // compute t (equation 3) 
	float t = -(dot(N, ray.Origin) - d) / NdotRayDirection;
    // check if the triangle is in behind the ray 
	if (t < 0) 
		return false;
    // the triangle is behind 
	// compute the intersection point using equation 1 
	vec3 P = ray.Origin + t * ray.Direction;
    // // Step 2: inside-outside test // 
	vec3 C;
    // vector perpendicular to triangle's plane 
	// edge 0 
	vec3 edge1 = v2 - v1;
    vec3 VP1 = P - v1;
    C = cross(edge1, VP1);
    if (dot(N, C) < 0)
		return false;
    // P is on the right side 
	// edge 1 
	vec3 edge2 = v3 - v2;
    vec3 VP2 = P - v2;
    C = cross(edge2, VP2);
    if (dot(N, C) < 0) 
		return false;
    // P is on the right side 
	// edge 2 
	vec3 edge3 = v1 - v3;
    vec3 VP3 = P - v3;
    C = cross(edge3, VP3);
    if (dot(N, C) < 0) 
		return false;
    // P is on the right side; 
	time = t;
    return true;
    // this ray hits the triangle
}
/************************************************* SUPPORT FUNCTIONS **************************************************/

SRay GenerateRay ( void )
{
	vec2 coords = glPosition.xy * uCamera.Scale;
	vec3 direction = uCamera.View + uCamera.Side * coords.x + uCamera.Up * coords.y;
	return SRay ( uCamera.Position, normalize(direction) );
}


vec3 Phong ( SIntersection intersect, SLight currLight, vec3 viewDirection, float shadowing )
{
    vec3 light = normalize ( currLight.Position - intersect.Point );
    vec3 view = normalize ( uCamera.Position - intersect.Point );
    float diffuse = max ( dot ( light, intersect.Normal ), 0.0 );
    // или - viewDirection
    vec3 reflected = reflect ( -view, intersect.Normal );
    float specular = pow ( max ( dot ( reflected, light ), 0.0 ), intersect.LightCoeffs.w );
    return intersect.LightCoeffs.x * intersect.Color +
		   intersect.LightCoeffs.y * diffuse * intersect.Color * shadowing +
		   intersect.LightCoeffs.z * specular * Unit;
}

/* ENGINE ********************************************************/

bool Raytrace ( SRay ray, float start, float final, inout SIntersection intersect )
{
    bool result = false;
    float test = start;
    intersect.Time = final;
    for(int j = 0; j < imageSize(uSpheres); j++)
	{
        SSphere Sphere = SSphere(imageLoad(uSpheres, j).xyz, imageLoad(uSpheres, j).w);
        if ( IntersectSphere (Sphere, ray, start, final, test ) && test < intersect.Time )
		{
            intersect.Time = test;
            intersect.Point = ray.Origin + ray.Direction * test;
            intersect.Normal = normalize ( intersect.Point - Sphere.Center );
            intersect.Color = uMaterials[6].Color;
            intersect.LightCoeffs = uMaterials[6].LightCoeffs;
            intersect.ReflectionCoef = uMaterials[6].ReflectionCoef;
            intersect.RefractionCoef = uMaterials[6].RefractionCoef;
            intersect.MaterialType = uMaterials[6].MaterialType;
            result = true;
        }
	}

	for(int j = 0; j < imageSize(uIndexes); j++)
	{
        int vertex1 =  int(imageLoad(uIndexes, j).x);
        int vertex2 =  int(imageLoad(uIndexes, j).y);
        int vertex3 =  int(imageLoad(uIndexes, j).z);
        STriangle triangle = STriangle(imageLoad(uPoints, vertex1).xyz, imageLoad(uPoints, vertex2).xyz, imageLoad(uPoints, vertex3).xyz, 1);
        if(RayTriangleIntersection(ray, triangle.v1, triangle.v2, triangle.v3, test) && test < intersect.Time )
		{
            intersect.Time = test;
            intersect.Point = ray.Origin + ray.Direction * test;
            intersect.Normal = normalize ( cross(triangle.v1 - triangle.v2, triangle.v3 - triangle.v2) );
            int material = int(imageLoad(uIndexes, j).w);
            intersect.Color = uMaterials[material].Color;
            intersect.LightCoeffs = uMaterials[material].LightCoeffs;
            intersect.ReflectionCoef = uMaterials[material].ReflectionCoef;
            intersect.RefractionCoef = uMaterials[material].RefractionCoef;
            intersect.MaterialType = uMaterials[material].MaterialType;
            result = true;
        }

	}
	return result;
}

float Shadow(SLight currLight, SIntersection intersect)
{
    // Point is lighted
	float shadowing = 1.0;
    // Vector to the light source
	vec3 direction = normalize(currLight.Position - intersect.Point);
    // Distance to the light source
	float distanceLight = distance(currLight.Position, intersect.Point);
    // Generation shadow ray for this light source
	SRay shadowRay = SRay(intersect.Point + direction * EPSILON, direction);
    // ...test intersection this ray with each scene object
	SIntersection shadowIntersect;
    shadowIntersect.Time = BIG;
    // trace ray from shadow ray begining to light source position
	if(Raytrace(shadowRay, 0, distanceLight, shadowIntersect))
	{
        // this light source is invisible in the intercection point
		shadowing = 0.0;
    }
	return shadowing;
}


float Fresnel(const vec3 I, const vec3 N, const float ior)
{
    float kr;
    float cosi = clamp(-1, 1, dot(I,N));
    float etai = 1, etat = ior;
    if (cosi > 0) 
	{
        float temp = etai;
        etai = etat;
        etat = temp;
    }

	// Compute sini using Snell's law
	float sint = etai / etat * sqrt(max(0.f, 1 - cosi * cosi));
    // Total internal reflection
	if (sint >= 1) 
	{
        kr = 1;
        return kr;
    }
	else 
	{
        float cost = sqrt(max(0.f, 1 - sint * sint));
        cosi = abs(cosi);
        float Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost));
        float Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost));
        return kr = (Rs * Rs + Rp * Rp) / 2;
    }

// As a consequence of the conservation of energy, transmittance is given by:
// kt = 1 - kr;
} 

/* ENTRY POINT *****************************************************/
const int MAX_STACK_SIZE = 10;
const int MAX_TRACE_DEPTH = 8;
STracingRay stack[MAX_STACK_SIZE];
int stackSize = 0;
bool pushRay(STracingRay secondaryRay)
{
	if(stackSize < MAX_STACK_SIZE - 1 && secondaryRay.depth < MAX_TRACE_DEPTH)
	{
		stack[stackSize] = secondaryRay;
		stackSize++;
		return true;
	}
	return false;
}

bool isEmpty()
{
	if(stackSize < 0)
		return true;
	return false;
}

STracingRay popRay()
{
	stackSize--;
	return stack[stackSize];	
}

void main ( void )
{

    // Generate primary ray from camera
	SRay ray = GenerateRay();

    float start = 0;
    float final = BIG;
    vec3 resultColor = Zero;
    STracingRay sray = STracingRay(ray, 1, 0);
    pushRay(sray);
    while(!isEmpty())
    {
        STracingRay sray = popRay();
        ray = sray.ray;
        SIntersection intersect;
        intersect.Time = BIG;
        start = 0;
        final = BIG;
        if (Raytrace(ray, start, final, intersect)) 
		{
			switch(intersect.MaterialType)
			{
			case DIFFUSE_REFLECTION:
			{
                float shadowing = Shadow(uLight, intersect);
                resultColor += sray.contribution * Phong ( intersect, uLight, -normalize(ray.Direction), shadowing );
				break;
            }
			case MIRROR_REFLECTION: 
			{
                if(intersect.ReflectionCoef < 1)
				{
                    float shadowing = Shadow(uLight, intersect);
                    resultColor += (1 - intersect.ReflectionCoef) * Phong ( intersect, uLight, -normalize(ray.Direction), shadowing );
                }
				vec3 reflectDirection = reflect(ray.Direction, intersect.Normal);
                // creare reflection ray
				STracingRay reflectRay = STracingRay(SRay(intersect.Point + reflectDirection * EPSILON, reflectDirection), sray.contribution * intersect.ReflectionCoef, sray.depth + 1);
                pushRay(reflectRay);
				break;
            }
			case REFRACTION:
			{
                bool outside = (dot(ray.Direction, intersect.Normal) < 0);					
                vec3 bias = EPSILON * intersect.Normal;
                float ior = outside ? 1.0/intersect.RefractionCoef : intersect.RefractionCoef;
				int signOut = outside ? 1 : -1;
                float kr = Fresnel(ray.Direction, intersect.Normal * signOut, ior);
                // compute refraction if it is not a case of total internal reflection
				kr = 0.99;
				if (kr < 1) 
				{
                    vec3 refractionDirection = normalize(refract(ray.Direction,  intersect.Normal * signOut, ior));
					vec3 refractionRayOrig = intersect.Point + EPSILON * refractionDirection;
                    STracingRay refractRay = STracingRay(SRay(refractionRayOrig, refractionDirection), sray.contribution * kr, sray.depth + 1);
                    pushRay(refractRay);
               }
		
			//	vec3 reflectionDirection = normalize(reflect(ray.Direction, intersect.Normal));
            //  vec3 reflectionRayOrig = outside ? intersect.Point + bias : intersect.Point - bias;
            //  STracingRay reflectionRay = STracingRay(SRay(reflectionRayOrig, reflectionDirection), sray.contribution * (1 - kr), sray.depth + 1);
            //  pushRay(reflectionRay);
			//	break;
            }
			} // case
			} //  if (Raytrace(ray, start, final, intersect)) 
		} // while(!isEmpty())

	FragColor = vec4 ( resultColor, 1.0 );
}


