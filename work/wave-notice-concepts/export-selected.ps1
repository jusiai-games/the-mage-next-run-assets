$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$out=Join-Path $PSScriptRoot '../../exports/v1/wave-notices'
New-Item -ItemType Directory -Force $out | Out-Null
function SaveArt($bitmap,$name){
    $bitmap.Save((Join-Path $out "$name.png"),[Drawing.Imaging.ImageFormat]::Png)
    $bitmap.Dispose()
}
foreach($type in @('buff','penalty')){
    $buff=$type -eq 'buff'
    $accent=if($buff){'#69edb5'}else{'#ff815f'}
    $shade=if($buff){'#284a46'}else{'#592d3c'}
    $dark=if($buff){'#183534'}else{'#401e2e'}
    $card=[Drawing.Bitmap]::new(197,43)
    $g=[Drawing.Graphics]::FromImage($card)
    Poly @(3,0,194,0,197,3,197,40,194,43,3,43,0,40,0,3) $accent
    Rect 2 2 193 39 $dark
    Rect 4 4 28 35 $shade
    if($buff){
        Poly @(12,21,17,24,23,17,25,19,17,27,11,23) $accent
    }else{
        Rect 17 16 2 8 $accent
        Rect 17 26 2 2 $accent
    }
    $g.Dispose()
    SaveArt $card "$type-card"
}
foreach($result in @('victory','defeat')){
    $color=if($result -eq 'victory'){'#315e4b'}else{'#803f44'}
    $rule=[Drawing.Bitmap]::new(163,7)
    $g=[Drawing.Graphics]::FromImage($rule)
    Rect 0 3 163 1 $color
    Poly @(81,0,85,3,81,7,77,3) $color
    $g.Dispose()
    SaveArt $rule "$result-rule"
}
$mask=[Drawing.Bitmap]::new(1576,86)
$g=[Drawing.Graphics]::FromImage($mask)
for($f=0;$f -lt 16;$f++){
    $x=($f%8)*197
    $y=[int][math]::Floor($f/8)*43
    if($f -eq 15){continue}
    for($py=0;$py -lt 43;$py+=2){
        $noise=if($f -eq 0){0}else{(($py*17)%11)-5}
        $edge=[int][math]::Max(0,[math]::Min(197,$f*14+$noise))
        if($edge -lt 197){Rect ($x+$edge) ($y+$py) (197-$edge) ([math]::Min(2,43-$py)) '#ffffff'}
    }
}
$g.Dispose()
SaveArt $mask 'erase-mask'
foreach($type in @('buff','penalty')){
    $buff=$type -eq 'buff'
    $bright=if($buff){'#b8ffe0'}else{'#ffb197'}
    $accent=if($buff){'#69edb5'}else{'#ff815f'}
    $sheet=[Drawing.Bitmap]::new(1632,110)
    $g=[Drawing.Graphics]::FromImage($sheet)
    for($f=1;$f -lt 15;$f++){
        $x=($f%8)*204 ; $y=[int][math]::Floor($f/8)*55
        for($i=0;$i -lt 15;$i++){
            $px=$f*14+($i*17+$f*11)%23-11
            $py=($i*13+$f*7)%39+3
            $py+=if($buff){-($i%6)}else{$i%6}
            $w=if($buff){1+$i%2}else{2+$i%3}
            if($px -lt 0 -or $px+$w -gt 204 -or $py -lt 0 -or $py+2 -gt 55){continue}
            Rect ($x+$px) ($y+$py) $w (1+$i%2) $(if($i%3 -eq 0){$bright}else{$accent})
        }
    }
    $g.Dispose()
    SaveArt $sheet "$type-erase"
}
& ffmpeg -hide_banner -loglevel error -y -i (Join-Path $PSScriptRoot 'stage-results.png') -vf 'crop=844:242:12:307' -frames:v 1 (Join-Path $out 'result-preview.png')
if($LASTEXITCODE -ne 0){throw 'Result preview export failed'}
& ffmpeg -hide_banner -loglevel error -y -i (Join-Path $PSScriptRoot 'wave-effects.gif') -filter_complex 'crop=844:151:12:397,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none' -loop 0 (Join-Path $out 'wave-preview.gif')
if($LASTEXITCODE -ne 0){throw 'Wave preview export failed'}
