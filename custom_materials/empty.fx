// Name: Empty
// Author: gubFS
// Description: An empty Custom Material, that just uses the models texture

const float4x4 matWorldViewProj;
const float4x4 matWorld;

texture entSkin1;
sampler TextureMapSampler = sampler_state
{
    Texture = <entSkin1>;
    AddressU  = Wrap;
    AddressV  = Wrap;
};

void EmptyVS(
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

float4 EmptyPS(
    in float2 InTex: TEXCOORD0,
    in float3 InNormal: TEXCOORD1): COLOR
{
    float4 color = tex2D(TextureMapSampler, InTex);
    return color;
}

technique EmptyTechnique
{
    pass P0
    {
        alphaBlendEnable = true;
        VertexShader = compile vs_3_0 EmptyVS();
        PixelShader  = compile ps_3_0 EmptyPS();
    }
}
