// Name: XRay Geometry
// Author: Superku, with refactor and modification by gubFS
// Description: The normal XRay Geometry material from the game, but with added ability to control more of the XRray effect

// skill1; Border Distance; How far away from the player the border of the XRay should be. Can be a negative value to flip the XRay effect
// skill2; Border Size; The size of the border color effect

const float4x4 matWorldViewProj;
const float4x4 matWorld;
const float4x4 matView;

const float4 vecSunDir;
const float4 vecViewDir;
const float4 vecViewPos;

const float4 vecSkill41;
const float4 vecSkill45;

const float3 playerPosLocal_var;

const float fAlbedo;
const float fAmbient;

texture highlights_tga_bmap;
sampler HighlightMapSampler = sampler_state{
    Texture = <highlights_tga_bmap>;
    AddressU  = Clamp;
    AddressV  = Clamp;
};

texture shadowmap_bmap;
sampler DepthSampler = sampler_state{
    Texture = <shadowmap_bmap>;
    minfilter = none;
    magfilter = none;
    mipfilter = none;
};

texture entSkin1;
sampler LookupMapSampler = sampler_state{
    Texture = <entSkin1>;
    AddressU  = Mirror;
    AddressV  = Mirror;
};

const float4x4 matEffect1;
float4 DoKuDepthFromWorldPos(float4 worldPos){
    return mul(worldPos, matEffect1);
}

const float fDark = 0.65;
const float fBright = 1.0;
const float fDepthOffset = 0.995;
float fDist(float4 DepthCoord, float fDepth){
    return tex2Dproj(DepthSampler, DepthCoord).r < (fDepth * fDepthOffset) ? fDark : fBright;
}

const float4 fTaps_PCF[9] = {
    {-1.0,-1.0, 0.0, 0.0},
    {-1.0, 0.0, 0.0, 0.0},
    {-1.0, 1.0, 0.0, 0.0},
    { 0.0,-1.0, 0.0, 0.0},
    { 0.0, 0.0, 0.0, 0.0},
    { 0.0, 1.0, 0.0, 0.0},
    { 1.0,-1.0, 0.0, 0.0},
    { 1.0, 0.0, 0.0, 0.0},
    { 1.0, 1.0, 0.0, 0.0}
};
const float fPCF = 0.00075;
float DoKuShadow(float4 InDepth)
{
    float fShadow = 0.;
    for (int i = 0; i < 9; i++){
        float4 fTap = InDepth + fPCF * fTaps_PCF[i];
        fShadow += fDist(fTap, InDepth.z) / 9.;
    }

    return fShadow;
}

void DiffuseVS(
    in float4 InPos: POSITION,
    in float3 InNormal: NORMAL,
    in float2 InTex: TEXCOORD0,
    in float2 InTex2: TEXCOORD1,
    out float4 OutPos: POSITION,
    out float4 OutTex: TEXCOORD0,
    out float3 OutNormal: TEXCOORD1,
    out float2 OutLookup: TEXCOORD2,
    out float4 OutWorldPos: TEXCOORD3,
    out float3 OutLightDiff: TEXCOORD4,
    out float4 OutDepth: TEXCOORD5)
{
    OutPos = mul(InPos, matWorldViewProj);
    OutNormal = normalize(mul(InNormal, matWorld));
    OutTex.xy = InTex;
    OutTex.zw = InTex2 - 1.;
    OutLookup = OutNormal * 0.25 + 0.5;
    OutWorldPos = mul(InPos, matWorld);
    OutLightDiff.xy = (playerPosLocal_var.xz - OutWorldPos.xy) * 0.002125;
    OutLightDiff.z = -0.125;
    OutDepth = DoKuDepthFromWorldPos(OutWorldPos);
}

float4 DiffusePS(
    in float4 InTex: TEXCOORD0,
    in float3 InNormal: TEXCOORD1,
    in float2 InLookup: TEXCOORD2,
    in float4 InWorldPos: TEXCOORD3,
    in float3 InLightDiff: TEXCOORD4,
    in float4 InDepth: TEXCOORD5): COLOR
{
    InNormal = normalize(InNormal);

    float3 InSunDir = -normalize(float3(4.75, -8., 3.));
    float pre_diffuse = saturate(dot(InSunDir, InNormal));
    float diffuse = 0.6 + 0.4 * pre_diffuse;
    float3 R = normalize(2 * dot(InNormal, InSunDir) * InNormal - InSunDir);
    float specular = pow(saturate(-R.z), 32);

    float highlight = tex2D(HighlightMapSampler, InLookup);
    float4 color = tex2D(LookupMapSampler, InTex);
    color.rg += InNormal.xy * 0.1;
    float4 final = color * (diffuse + specular * 0.25 + highlight * highlight * 0.5) - 0.0985;
    float color_factor = 1.; // color_factor is supposed to be fAlbedo, but it doesn't seem to work in custom materials :/
    final = lerp(highlight, final, color_factor);

    // player light
    float len = saturate(1. - length(InLightDiff.xy));
    float player_diffuse = saturate(dot(normalize(InLightDiff), InNormal));
    float player_light_factor = len * len * player_diffuse;
    final += player_light_factor * 0.5;

    // xray
    const float dist_from_player = length(InWorldPos.xy - playerPosLocal_var.xz);
    const float border_dist = vecSkill41.x;
    const float border_size = max(vecSkill41.y, 0.001);
    const float dist_outside_border = dist_from_player - abs(border_dist);
    const float border_factor = saturate(abs(dist_outside_border) / border_size);
    const float4 border = float4(0.5, 0.3, 0.275, 1.) * (border_factor + 0.1);
    final = lerp(final, border, 0.65 * step(border_factor, 0.999));
    clip(dist_outside_border * sign(border_dist));

    final *= 1. + fAmbient;

    return final * DoKuShadow(InDepth);
}

technique DiffuseTechnique
{
    pass P0
    {
        zWriteEnable = true;
        alphaBlendEnable = false;
        VertexShader = compile vs_3_0 DiffuseVS();
        PixelShader  = compile ps_3_0 DiffusePS();
    }
}
