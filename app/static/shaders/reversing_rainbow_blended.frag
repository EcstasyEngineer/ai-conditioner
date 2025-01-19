#ifdef GL_ES
precision highp float;
#endif

uniform float iTime;
uniform vec2  iResolution;

// Spiral parameters
const float iTimeScale    = 3.8;
const float spiralDensity = 50.0;
const float boundaryBuffer = 1.0 / 9.0;  // Blend region width near each boundary

// Returns a rainbow color based on spiral angle
vec3 getSpiralColor(float angle, float radius)
{
    // Spiral position
    float spiral = mod(angle + radius * spiralDensity, 6.2831); // 2π ~ 6.2831
    // Rainbow color mapping
    float r = 0.5 + 0.5 * cos(spiral);
    float g = 0.5 + 0.5 * cos(spiral + 2.094); // ~120° offset
    float b = 0.5 + 0.5 * cos(spiral + 4.188); // ~240° offset
    return vec3(r, g, b);
}

void main(void)
{
    // Normalize coordinates: [-1,1] in the longer axis, keep aspect ratio
    vec2 uv = (gl_FragCoord.xy / iResolution.xy) * 2.0 - 1.0;
    if (iResolution.y > iResolution.x) {
        uv.y *= iResolution.y / iResolution.x;
    } else {
        uv.x *= iResolution.x / iResolution.y;
    }

    float radius = length(uv);
    float angle  = atan(uv.y, uv.x);

    // -------------------------------------
    // 1) Identify which "region" we're in
    //    regionIndex = floor(radius * 3.0)
    //    => 0 => [0..1/3), 1 => [1/3..2/3), 2 => [2/3..1.0)
    // -------------------------------------
    float regionIndex = floor(radius * 3.0);

    // If radius >= 1.0, clamp to regionIndex=2 so we don't go out of bounds
    // (in practice you can decide how you want to handle beyond radius=1).
    regionIndex = clamp(regionIndex, 0.0, 2.0);

    // -------------------------------------
    // 2) Check if the current region is reversed
    //    isReverse = mod(regionIndex,2) -> 0 => normal, 1 => reversed
    // -------------------------------------
    float isReverseCurrent = mod(regionIndex, 2.0);

    // -------------------------------------
    // 3) Compute the boundary to the next region
    //    nextBoundary = (regionIndex + 1.0) / 3.0
    // -------------------------------------
    // If regionIndex=2, you could either skip or treat boundary=1.0
    float nextBoundary = (regionIndex < 2.0)
        ? (regionIndex + 1.0) / 3.0
        : 1.0;  // or skip blending if radius>1

    // Distance to that boundary
    float distFromBoundary = abs(radius - nextBoundary);

    // -------------------------------------
    // 4) Blend factor near boundary
    //    If dist < boundaryBuffer => some blending
    //    else fully in the current region
    // -------------------------------------
    float blendFactor = 0.0;
    if (distFromBoundary < boundaryBuffer) {
        blendFactor = 1.0 - distFromBoundary / boundaryBuffer;
        blendFactor = clamp(blendFactor, 0.0, 1.0);
    }

    // -------------------------------------
    // 5) Figure out the orientation for the NEXT region
    //    next region index = regionIndex+1
    // -------------------------------------
    float isReverseNext = mod(regionIndex + 1.0, 2.0); // 0 => normal, 1 => reversed

    // -------------------------------------
    // 6) Compute both spirals
    // -------------------------------------
    float angleNormal  = angle + iTime * iTimeScale;
    float angleReverse = angle - iTime * iTimeScale;

    vec3 colorNormal  = getSpiralColor(angleNormal,  radius);
    vec3 colorReverse = getSpiralColor(angleReverse, radius);

    // -------------------------------------
    // 7) Determine the primary color (current region)
    //    and the secondary color (adjacent region)
    // -------------------------------------
    vec3 colorPrimary   = (isReverseCurrent < 0.5) ? colorNormal : colorReverse;
    vec3 colorSecondary = (isReverseNext    < 0.5) ? colorNormal : colorReverse;

    // Start with the primary color
    vec3 finalColor = colorPrimary;

    // Near the boundary, blend in the adjacent region color
    if (blendFactor > 0.0) {
        finalColor = mix(colorPrimary, colorSecondary, blendFactor);
    }

    gl_FragColor = vec4(finalColor, 1.0);
}
