$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$out = $PSScriptRoot
$root = Join-Path $out '../..'
function Pixel($x,$y,$w,$h,$color) {
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.FillRectangle($brush,[int]$x,[int]$y,[int]$w,[int]$h)
    $brush.Dispose()
}
function Traveler($sprite) {
    $palette=@{
        K='#221c2e'; D='#4e3039'; N='#743a3b'; B='#a34d40'; L='#cb684a'
        W='#eea16c'; H='#ffe0b2'; S='#ac6857'; F='#f5bb87'; E='#241e32'; I='#fff1d6'; U='#466e9a'
    }
    $sprite.SetPixel(24,7,[Drawing.Color]::Transparent)
    $sprite.SetPixel(24,8,[Drawing.Color]::Transparent)
    # Head region only. Dots clear the original hood outside the new hair.
    $rows=@(
        '...............'
        '...............'
        '...KKKKKKKK....'
        '..KWWWLLBBNK...'
        '..KWLBBNNLBKK..'
        '.KLLBNWLLBNBLK.'
        '..KNDNBBNLBLKK.'
        '...KBLNKNFSKK..'
        '..KNNBKSHFFK...'
        '....KDKSFEFK...'
        '....KDKSFUFK...'
        '.....KKSFFK....'
        '......KSSK.....'
    )
    for($y=0;$y -lt $rows.Count;$y++){
        for($x=0;$x -lt $rows[$y].Length;$x++){
            $key=[string]$rows[$y][$x]
            $color=if($key -eq '.') {[Drawing.Color]::Transparent} else {[Drawing.ColorTranslator]::FromHtml($palette[$key])}
            $sprite.SetPixel(($x+9),($y+1),$color)
        }
    }
}
function RetroMage {
    $palette=@{
        K='#211c2a'; D='#332844'; N='#524069'; B='#806294'; R='#6c3135'
        V='#be583f'; Y='#ef8a54'; S='#b47555'; F='#f3b979'; H='#ffe3af'
        T='#694331'; W='#a97348'; G='#e7b464'; A='#58b9aa'; C='#d8ffe5'
    }
    $rows=@(
        '....KKKK...........'
        '..KKRVVKK..........'
        '.KRVYVVVKK.........'
        '.KVYVRRVVK.....K...'
        '..KRVVYFSK....KCK..'
        '..KRVVKFFK....KAK..'
        '...KRKSFFK....KGK..'
        '....KKFFK.....KWK..'
        '...KBNKHK.....KWK..'
        '..KBBNDHGKK...KWK..'
        '..KBNNDBNNKK..KWK..'
        '..KBNDBNKFFKKKWK..'
        '..KNDBNKFFSGKGWK..'
        '.KNDNDKKSGGKKKWK..'
        '.KNDDKTWWKDK..WK..'
        '.KNDDKWGWKDNK.WK..'
        '.KDDDKTWWKBNK.WK..'
        'KDDDKKKTTKNDK.WK..'
        'KKKK.KNDKNDK..WK..'
        '.....KDWKDWK..WK..'
        '....KTWWKTWWK.KK..'
        '....KKKK.KKKK......'
    )
    for($y=0;$y -lt $rows.Count;$y++){
        for($x=0;$x -lt $rows[$y].Length;$x++){
            $key=[string]$rows[$y][$x]
            if($key -ne '.'){ Pixel ($x+7) ($y+6) 1 1 $palette[$key] }
        }
    }
}
function OriginalPoseMage($sprite) {
    Traveler $sprite
    $cloak=@{'292d49'='#372b49';'3c456b'='#4d3b61';'4a547d'='#64517c';'626b97'='#826898'}
    for($y=14;$y -lt 28;$y++){
        for($x=0;$x -lt 32;$x++){
            $pixel=$sprite.GetPixel($x,$y)
            if($pixel.A -eq 0){continue}
            $rgb=$pixel.Name.Substring(2)
            if($cloak.ContainsKey($rgb)){
                $sprite.SetPixel($x,$y,[Drawing.ColorTranslator]::FromHtml($cloak[$rgb]))
            }
        }
    }
    # Keep the original staff grip, add the crystal above its wooden socket.
    Pixel 25 8 2 5 '#221c2e'
    Pixel 24 9 4 2 '#221c2e'
    Pixel 25 9 2 2 '#67c7b6'
    Pixel 26 9 1 1 '#dcffea'
    Pixel 25 11 2 1 '#cca064'
    Pixel 15 15 1 1 '#e9b470'
    Pixel 14 16 1 1 '#b98557'
}
function OpenBitmap($path) { [Drawing.Bitmap]::new((Join-Path $root $path)) }
function Label($value,$x,$y,$size,$color) {
    $font=[Drawing.Font]::new('Malgun Gothic',$size,[Drawing.GraphicsUnit]::Pixel)
    $brush=[Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.DrawString($value,$font,$brush,[single]$x,[single]$y)
    $font.Dispose()
    $brush.Dispose()
}
function Frame($index) {
    $sprite=[Drawing.Bitmap]::new(32,32)
    $g=[Drawing.Graphics]::FromImage($sprite)
    if ($index -eq 0) {
        $g.DrawImage($original,[Drawing.Rectangle]::new(0,0,32,32),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
    } else {
        if ($index -eq 1) {
            RetroMage
        } else {
            $g.DrawImage($original,[Drawing.Rectangle]::new(0,0,32,32),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
            OriginalPoseMage $sprite
        }
        foreach ($y in 0..31) {
            foreach ($x in 0..31) {
                $alpha=$sprite.GetPixel($x,$y).A
                if ($alpha -notin @(0,255) -or ($alpha -gt 0 -and $y -ge 28)) {
                    throw "Invalid pixel at $x,$y"
                }
            }
        }
        $sprite.Save((Join-Path $out "$($ids[$index])-wizard.png"),[Drawing.Imaging.ImageFormat]::Png)
    }
    $g.Dispose()
    $sprite
}
$ids=@('original','retro','original-pose')
$labels=@('기존','A · 전투 도트','B · 얼굴 윤곽 수정')
$original=OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$terrain=OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$board=[Drawing.Bitmap]::new(574,332)
$g=[Drawing.Graphics]::FromImage($board)
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
$g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::AntiAliasGridFit
Pixel 0 0 574 332 '#242735'
Label '마법사 주인공 비교' 20 14 24 '#fff0d5'
Label '4배 확대  ·  초원 위 1배' 20 49 14 '#d2c3cb'
for ($i=0; $i -lt 3; $i++) {
    $x=18+182*$i
    $sprite=Frame $i
    Pixel $x 80 174 234 '#343b50'
    Label $labels[$i] ($x+10) 88 15 '#ffe0ac'
    Pixel ($x+8) 116 158 136 '#505a70'
    $g.DrawImage($sprite,[Drawing.Rectangle]::new(($x+23),119,128,128))
    $g.DrawImage($terrain,[Drawing.Rectangle]::new(($x+7),264,160,42),0,50,160,42,[Drawing.GraphicsUnit]::Pixel)
    $g.DrawImage($sprite,($x+15),265,32,32)
    $sprite.Dispose()
}
$board.Save((Join-Path $out 'comparison.png'),[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$board.Dispose()
$terrain.Dispose()
$original.Dispose()



























