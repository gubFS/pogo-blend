// Name: Example
// Author: Superku, with comments and refactor by gubFS
// Description: A simple material that changes the vertices and colors of the model. Can be used to learn more about Custom Materials, or as a starting point for making your own. Custom Materials is written in High-Level Shader Language (HLSL), which has much online support that you can refer to.

// You can name skills in comments, so they will be shown in PogoBlend, like so:
// skill1; Time power; How much effect the time should have

// here's some commonly used values given by the engine. More exists, that can be found in the manual: http://manual.conitec.net/
const float4x4 matWorldViewProj; // the model view projection matrix
const float4x4 matWorld; // the transformation matrix of the entity
const float4x4 matView; // the transformation matrix of the camera
const float4 vecViewDir; // the direction of the camera (normalized)
const float4 vecViewPos; // the position of the camera

float3 playerPosLocal_var; // the player position

// skills that can be set with the 'Skill Set' action. They contain 4 skills each, in their x, y, z and w variables.
const float4 vecSkill41;
const float4 vecSkill45;

// vecTime.x is "time_step", which is how long a step of time is, aka it is affected by your FPS
// vecTime.w is "total_ticks", aka how long the game has been running. There is 16 whole ticks every second
const float4 vecTime;

const float fAmbient; // ambient value between 0..1
const float fAlbedo; // albedo value between 0..1

// mesh textures
texture entSkin1;
texture entSkin2;
texture entSkin3;
texture entSkin4;

// sampler to sample the first texture
sampler TextureMapSampler = sampler_state
{
    Texture = <entSkin1>;
    AddressU  = Wrap;
    AddressV  = Wrap;
};

// Vertex Shader - this is where the vertices of the model can be altered
void ExampleVS(
    in float4 InPos: POSITION,
    in float3 InNormal: NORMAL,
    in float2 InTex: TEXCOORD0,
    out float4 OutPos: POSITION,
    out float2 OutTex: TEXCOORD0,
    out float3 OutNormal: TEXCOORD1)
{
    float time_power = max(vecSkill41.x, 0.) ? vecSkill41.x : 0.25;
    float time = vecTime.w * time_power;
    float3 modulation = sin(time + InPos.yzx * 0.175) * 7.;

    InPos.xyz += InNormal * modulation;
    InNormal += modulation * 0.05;

    OutPos = mul(InPos, matWorldViewProj);
    OutNormal = mul(InNormal, matWorld);
    OutTex.xy = InTex;
}

// Pixel Shader - this is where the colors of the model can be altered
float4 ExamplePS(
    in float2 InTex: TEXCOORD0,
    in float3 InNormal: TEXCOORD1): COLOR
{
    InNormal = normalize(InNormal);

    float3 InSunDir = -normalize(float3(4.75, -8, 3.));
    float diffuse = 0.7 + 0.5 * saturate(dot(InSunDir, InNormal));

    float4 color = tex2D(TextureMapSampler, InTex * 2.);
    color.rg += InNormal.xy * 0.3;
    float4 final = color * diffuse + InNormal.z * 0.2;

    return final;
}

// this is where it is all put together, by defining which shaders are in use and the options
technique ExampleTechnique
{
    pass P0
    {
        alphaBlendEnable = true; // change this to false to disable transparency
        VertexShader = compile vs_3_0 ExampleVS();
        PixelShader  = compile ps_3_0 ExamplePS();
    }
}
