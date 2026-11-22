$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'render-variants.ps1') -DefinitionsOnly

$export=Join-Path $PSScriptRoot '../../exports/v1'
$out=Join-Path $export 'wood-spell-cards/skill-art'
$data=Get-Content (Join-Path $export 'spell-effects/unity-slicing.json') -Raw | ConvertFrom-Json
$themes=@{
    fire=@{label='화염'; deep='#703833'; colors=@('#ae4e43','#ee7547','#ffb565','#fff0bb')}
    cold=@{label='냉기'; deep='#305c5e'; colors=@('#437d8e','#78cbbd','#a2e4e6','#edfffa')}
    lightning=@{label='번개'; deep='#274969'; colors=@('#4c6bb1','#73b8e2','#a2dfff','#f1f3ff')}
}
# Shape commands use palette index followed by coordinates, on a 28×26 canvas.
$art=@{
    'fire-bolt'='p1 2 20 13 13 11 12 24 7 26 10 24 15 17 17 18 19;r2 5 18 3 2;p3 15 15 24 9 24 13 20 15'
    'warmth'='e0 3 8 21 15;e1 6 12 15 10;p2 10 16 10 12 14 5 16 10 19 13 18 17 15 20 12 19;p3 13 17 14 12 17 16 16 19;r2 5 8 2 3;r2 21 6 2 4'
    'inferno'='p0 2 15 10 10 14 11 19 5 26 6 22 10 27 12 24 16 27 20 19 21 13 18 8 19;p1 4 15 13 13 18 9 24 8 20 13 25 14 22 17 24 19 16 17;p3 4 15 14 14 18 12 22 13 17 16 10 17'
    'blaze'='l0 2 23 9 19 15 20 20 15 26 15;p1 5 21 6 16 10 13 10 17 12 18 10 22;p2 14 20 13 17 16 12 19 10 18 15 21 17 18 21;p1 21 16 20 12 24 7 24 11 27 13 26 17'
    'fire-ball'='p0 2 21 8 12 11 12 15 7 22 5 26 9 26 16 22 20 17 22 12 20;p1 6 20 12 13 16 13 17 8 23 7 25 11 23 17 19 20;p2 13 16 17 13 18 9 23 9 24 13 20 18 16 18;p3 17 15 21 10 23 12 21 15'
    'fire-wall'='p0 2 20 4 13 7 10 8 15 11 12 13 4 16 8 17 14 20 11 22 6 23 12 26 15 26 20;p1 3 19 7 14 9 17 13 10 15 8 16 17 20 15 22 11 24 17 26 19;r2 3 19 23 3;r3 8 20 12 1'
    'enchant'='p0 4 22 8 17 7 13 11 14 20 5 24 4 23 9 14 18 14 21 11 20 7 24;p1 11 15 17 7 24 3 23 9 15 17;p3 13 16 21 7 23 6 22 9 15 17;r2 5 9 2 2;r2 22 15 2 2'
    'meteor'='p0 7 2 15 5 25 13 26 17 22 21 16 21 11 17 10 12 4 9 10 10;p1 11 5 20 10 24 14 24 18 21 20 16 19 13 15 13 12;p2 15 10 22 13 23 16 20 19 16 17 16 14;r3 19 14 3 3;l1 6 23 12 23 15 21 19 23 25 23'
    'fire-mastery'='p0 4 18 7 9 10 13 14 4 18 13 23 9 24 19 21 22 7 22;p2 6 17 8 12 11 16 14 8 17 16 21 13 22 18;r1 7 19 15 3;p3 12 18 14 14 17 18 14 21'
    'hydra'='l1 7 6 6 12 10 16 10 21;l1 14 4 15 10 14 21;l1 22 7 23 12 20 16 18 21;p2 3 6 7 4 11 6 10 9 6 9;p2 10 4 14 2 18 4 17 7 13 7;p2 18 7 23 5 26 7 25 10 21 10;r3 7 6 2 1;r3 14 4 2 1;r3 22 7 2 1;r0 8 21 13 2'
    'ice-bolt'='l0 3 20 13 15 10 15 17 10;p1 9 18 14 11 25 8 22 16 15 19;p3 13 16 17 12 23 9 20 14'
    'frozen-armor'='p0 5 8 14 4 23 8 22 17 14 23 6 17;p1 7 9 14 6 21 9 20 16 14 21 8 16;p2 10 10 14 8 18 10 17 15 14 18 11 15;l3 14 10 14 16;l3 11 13 17 13'
    'frost-nova'='e0 2 7 23 13;e1 3 9 21 9;e2 6 11 15 5;l3 11 13 16 13;r2 3 6 2 2;r2 22 19 2 2'
    'ice-blast'='p1 4 19 8 10 12 14 14 4 17 14 23 9 22 17 26 19 17 20 13 23 10 20;p3 9 18 12 16 14 10 15 17 20 16 16 20;r2 4 7 2 2;r2 22 5 2 3'
    'shiver-armor'='p0 3 20 5 11 9 16 13 6 17 16 22 10 25 18 21 22 7 22;p1 4 20 6 13 10 18 13 9 16 19 21 13 23 18 20 21;p3 12 17 13 10 15 18;r2 6 20 15 1'
    'glacial-spike'='p0 2 20 10 10 16 12 26 6 23 16 15 22;p1 4 19 11 13 17 14 25 7 22 15 15 20;p3 8 18 14 16 24 8 20 15 15 18'
    'blizzard'='l0 3 8 10 5 22 5 25 8;l2 10 8 4 16;l3 15 8 9 18;l2 21 9 15 18;l3 25 10 20 20;p1 3 22 7 18 12 20 15 18 20 20 25 19 24 23 4 23'
    'chilling-armor'='p0 3 20 3 13 8 6 14 4 21 7 25 13 25 20;l2 3 19 4 12 9 7 14 5 20 8 24 13 25 19;l1 5 19 23 19;l2 8 17 12 12 17 11 20 15;l3 12 12 15 14 18 12'
    'frozen-orb'='p0 7 7 12 4 18 5 23 10 23 16 18 21 10 21 5 16 5 11;p1 8 8 13 6 19 8 21 12 20 17 17 19 10 18 7 15;l3 8 13 12 10 18 10 20 13 17 16 12 16;r2 2 8 2 2;r2 24 18 2 2'
    'cold-mastery'='l1 14 3 14 23;l2 6 6 22 20;l2 6 20 22 6;l2 11 4 14 7 17 4;l2 11 22 14 19 17 22;p3 14 9 17 13 14 17 11 13'
    'charged-bolt'='l1 2 11 6 8 7 12 12 9;l2 8 17 12 13 13 17 18 12;l3 15 21 19 17 20 21 25 16;r1 22 9 2 2'
    'static-field'='e0 2 9 23 12;e1 4 11 19 8;l2 3 15 7 14 10 16 14 13 18 15 24 14;r3 13 8 2 3;r2 5 8 2 2;r2 21 8 2 2'
    'telekinesis'='p1 2 8 8 8 11 13 8 18 2 18 6 13;p1 26 8 20 8 17 13 20 18 26 18 22 13;p3 14 9 17 13 14 17 11 13;r2 13 5 2 2;r2 13 20 2 2'
    'nova'='p0 2 13 6 10 4 5 10 7 14 2 17 7 23 5 21 10 26 13 21 16 23 22 17 20 14 24 10 20 4 22 6 16;l2 4 13 9 10 8 7 12 9 14 5 16 9 20 8 19 11 23 13 18 15 19 19 16 17 14 21 12 17 8 19 9 15 4 13;p3 14 10 17 13 14 16 11 13'
    'lightning'='p0 2 11 8 11 11 8 16 11 26 11 26 17 17 16 13 19 9 16 2 16;l2 2 13 9 13 12 11 15 15 20 13 26 14;l3 2 14 25 14'
    'chain-lightning'='l1 3 18 8 16 7 11 14 8 16 12 21 11 25 6;l3 3 17 8 15 8 12 14 9 16 13 21 12 25 7;r2 2 16 3 4;r2 13 7 3 3;r2 23 5 3 3'
    'teleport'='p0 14 2 22 7 25 13 22 19 14 24 6 19 3 13 6 7;p2 14 5 21 9 23 13 20 17 14 21 8 17 5 13 8 9;p0 14 8 18 11 19 13 17 16 14 18 10 16 9 13 10 11;r3 13 10 2 7;r3 11 12 6 2'
    'thunder-storm'='p0 4 8 6 5 10 5 12 2 18 2 20 5 23 5 25 8 23 10 5 10;p1 8 6 12 4 18 4 22 7 8 8;p2 15 8 20 8 16 13 20 13 10 23 12 16 8 16;p3 15 9 17 9 13 15 17 14 12 20 13 15 10 15'
    'energy-shield'='e1 3 3 22 20;e2 5 5 18 16;p0 8 9 14 6 20 9 19 16 14 20 9 16;p2 10 10 14 8 18 10 17 15 14 17 11 15;l3 12 13 14 11 16 13 14 15 12 13'
    'lightning-mastery'='p0 14 2 23 7 25 15 19 22 9 22 3 15 5 7;l2 5 8 9 11 7 14 10 18;l2 23 8 19 11 21 14 18 18;p2 14 5 19 5 15 11 19 11 11 21 13 14 9 14;p3 14 7 16 7 12 13 15 13 12 17 13 13 11 13'
}
function DrawGlyph($shape,$colors){
    foreach($part in ($shape -split ';')){
        $kind=$part[0]
        $color=$colors[[int]::Parse([string]$part[1])]
        [int[]]$coords=($part.Substring(3) -split ' ')
        switch($kind){
            'p' { Poly $coords $color }
            'r' { Rect $coords[0] $coords[1] $coords[2] $coords[3] $color }
            'l' {
                $points=for($i=0;$i -lt $coords.Count;$i+=2){[Drawing.Point]::new($coords[$i],$coords[$i+1])}
                $pen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($color))
                $g.DrawLines($pen,[Drawing.Point[]]$points)
                $pen.Dispose()
            }
            'e' {
                $pen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($color))
                $g.DrawEllipse($pen,$coords[0],$coords[1],$coords[2],$coords[3])
                $pen.Dispose()
            }
        }
    }
}
function CenterTitle($x,$y,$name,$size,$color){
    $font=[Drawing.Font]::new('Malgun Gothic',$size,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
    $brush=Brush $color
    $format=[Drawing.StringFormat]::new()
    $format.Alignment='Center'
    $g.DrawString($name,$font,$brush,[single]$x,[single]$y,$format)
    $format.Dispose()
    $brush.Dispose()
    $font.Dispose()
}

$items=@($data.effects)
if($items.Count -ne 30 -or $art.Count -ne 30){throw 'Expected 30 effects and 30 unique glyph designs.'}
$preview=[Drawing.Bitmap]::new(1140,657)
$g=[Drawing.Graphics]::FromImage($preview)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#18202d'))
$g.TextRenderingHint='AntiAliasGridFit'
$g.InterpolationMode='NearestNeighbor'
$g.PixelOffsetMode='Half'
Label 19 12 '나무 명판 v1 · 주문 삽화 30종' 26 '#ffe5bd' $true
$manifest=@()
$hashes=[Collections.Generic.HashSet[string]]::new()
for($row=0;$row -lt 3;$row++){
    $tree=@('fire','cold','lightning')[$row]
    $theme=$themes[$tree]
    $effects=@($items | Where-Object tree -eq $tree)
    if($effects.Count -ne 10){throw "Expected 10 effects for $tree"}
    $folder=Join-Path $out $tree
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    $frame=CardFace 0 -1 @{deep=$theme.deep}
    $frame.Save((Join-Path $folder 'frame.png'),[Drawing.Imaging.ImageFormat]::Png)
    $y=62+$row*195
    Label 22 $y $theme.label 19 $theme.colors[2] $true
    for($i=0;$i -lt $effects.Count;$i++){
        $effect=$effects[$i]
        $id=[IO.Path]::GetFileNameWithoutExtension($effect.sheet)
        if(-not $art.ContainsKey($id)){throw "Missing art: $id"}
        $icon=[Drawing.Bitmap]::new(28,26)
        $display=$g
        $g=[Drawing.Graphics]::FromImage($icon)
        DrawGlyph $art[$id] $theme.colors
        $g.Dispose()
        $g=$display
        $opaque=0
        for($py=0;$py -lt 26;$py++){
            for($px=0;$px -lt 28;$px++){
                $a=$icon.GetPixel($px,$py).A
                if($a -notin 0,255){throw "Invalid alpha: $id"}
                if($a -eq 255){
                    if($px -in 0,27 -or $py -in 0,25){throw "Art touches canvas edge: $id"}
                    $opaque++
                }
            }
        }
        if($opaque -lt 20){throw "Insufficient visible art: $id"}
        $png=Join-Path $folder "$id.png"
        $icon.Save($png,[Drawing.Imaging.ImageFormat]::Png)
        if(-not $hashes.Add((Get-FileHash $png).Hash)){throw "Duplicate art: $id"}
        $card=[Drawing.Bitmap]::new($frame)
        $cardSurface=[Drawing.Graphics]::FromImage($card)
        $cardSurface.DrawImageUnscaled($icon,8,8)
        $cardSurface.Dispose()
        $icon.Dispose()
        $cx=22+$i*112
        $cy=$y+30
        $g.DrawImage($card,[Drawing.Rectangle]::new($cx,$cy,88,128))
        $card.Dispose()
        CenterTitle ($cx+44) ($cy+133) $effect.name 11 '#efe3d5'
        $manifest+=@{id=$id; name=$effect.name; element=$tree; image="$tree/$id.png"; frame="$tree/frame.png"; effectSheet="spell-effects/$($effect.sheet)"}
    }
    $frame.Dispose()
}
$g.Dispose()
$preview.Save((Join-Path $out 'preview.png'),[Drawing.Imaging.ImageFormat]::Png)
$preview.Dispose()
@{canvasPx=@(28,26); cardOriginPx=@(8,8); spells=$manifest} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 (Join-Path $out 'manifest.json')

