// Name: Renderchain
// Author: gubFS, with snippets from Superku
// Description: An example Custom Material that show you can sample the renderchain (screen output), to do some cool stuff. Here it is used to add some fake reflections, to models with geometry

const float4x4 matWorldViewProj;
const float4x4 matWorld;

texture highlights_tga_bmap;
sampler HighlightMapSampler = sampler_state{
    Texture = <highlights_tga_bmap>;
    AddressU  = Clamp;
    AddressV  = Clamp;
};

texture renderchain_bmap_bmap;
sampler2D renderchainSampler = sampler_state
{
    Texture = <renderchain_bmap_bmap>;
    AddressU        = Mirror; // or Clamp or Wrap
    AddressV        = Mirror;
};

texture entSkin1;
sampler TextureMapSampler = sampler_state
{
    Texture = <entSkin1>;
    AddressU  = Wrap;
    AddressV  = Wrap;
};

void RenderchainVS(
    in float4 InPos: POSITION,
    in float3 InNormal: NORMAL,
    in float2 InTex: TEXCOORD0,
    out float4 OutPos: POSITION,
    out float2 OutTex: TEXCOORD0,
    out float3 OutNormal: TEXCOORD1,
    out float3 OutProjTex: TEXCOORD2)
{
    OutPos = mul(InPos, matWorldViewProj);
    OutNormal = mul(InNormal, matWorld);
    OutTex = InTex;
    OutProjTex = OutPos.xyw;
}

float4 RenderchainPS(
    in float4 InTex: TEXCOORD0,
    in float3 InNormal: TEXCOORD1,
    in float3 InProjTex: TEXCOORD2): COLOR
{
    InProjTex.xy = InProjTex.xy / InProjTex.z;
    InProjTex.xy = InProjTex.xy * 0.5 + 0.5;
    InProjTex.y = 1.0 - InProjTex.y;

    InProjTex *= InNormal;

    float4 render = tex2D(renderchainSampler, InProjTex);
    float4 color = tex2D(TextureMapSampler, InTex);
    return color * render;
}

technique RenderchainTechnique
{
    pass P0
    {
        alphaBlendEnable = true;
        VertexShader = compile vs_3_0 RenderchainVS();
        PixelShader  = compile ps_3_0 RenderchainPS();
    }
}
