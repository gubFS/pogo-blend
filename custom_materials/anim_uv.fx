// Name: AnimUV
// Author: gubFS
// Description: Goes through the texture on the entity as a spritesheet from left to right top to bottom. Can be used to animate textures. Must be used with "Skill set" action.

// skill1; Columns; Number of columns (will be rounded down)
// skill2; Rows; Number of rows (will be rounded down)
// skill3; Total frames; The total number of frames (aka sprites in the sheet) (will be rounded down). Can be used to cut off empty frames at the end. If left at 0, the number of frames will be columns * rows
// skill4; Speed (seconds); The time in seconds that it takes to play the entire animation. If left at 0, it will take one second
// skill5; Start frame; The index of the frame that the animation should start at (will be rounded down)

const float4x4 matWorldViewProj;
const float4x4 matWorld;

const float4 vecSkill41;
const float4 vecSkill45;
const float4 vecTime;

texture entSkin1;
sampler TextureMapSampler = sampler_state
{
    Texture = <entSkin1>;
    AddressU  = Wrap;
    AddressV  = Wrap;
};

void AnimUVVS(
    in float4 InPos: POSITION,
    in float3 InNormal: NORMAL,
    in float2 InTex: TEXCOORD0,
    out float4 OutPos: POSITION,
    out float2 OutTex: TEXCOORD0,
    out float3 OutNormal: TEXCOORD1)
{
    OutPos = mul(InPos, matWorldViewProj);
    OutNormal = mul(InNormal, matWorld);
    OutTex = InTex;
}

float4 AnimUVPS(
    in float2 InTex: TEXCOORD0,
    in float3 InNormal: TEXCOORD1): COLOR
{
    int cols = max(int(vecSkill41.x), 1);
    int rows = max(int(vecSkill41.y), 1);
    int total_frames = max(int(vecSkill41.z), 0.) ? int(vecSkill41.z) : cols * rows;
    float seconds_to_play = max(vecSkill41.w, 0.) ? vecSkill41.w : 1.;
    int start_frame = max(int(vecSkill45.x), 0);
    float shading = saturate(vecSkill45.y);

    float x_gap = 1. / cols;
    float y_gap = 1. / rows;

    float seconds_per_frame = seconds_to_play / total_frames;
    int passed_frames = int(vecTime.w / 16. / seconds_per_frame);
    int frame = (start_frame + passed_frames) % total_frames;

    InTex.x = x_gap * (frame % cols) + InTex.x * x_gap;
    InTex.y = y_gap * floor(frame / cols) + InTex.y * y_gap;

    float4 color = tex2D(TextureMapSampler, InTex);

    return color;
}

technique AnimUVTechnique
{
    pass P0
    {
        alphaBlendEnable = true;
        VertexShader  = compile vs_3_0 AnimUVVS();
        PixelShader  = compile ps_3_0 AnimUVPS();
    }
}
