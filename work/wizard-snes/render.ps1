$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$out = $PSScriptRoot
$root = Join-Path $out '../..'
function Pixel($x,$y,$w,$h,$color) {
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.FillRectangle($brush,[int]$x,[int]$y,[int]$w,[int]$h)
    $brush.Dispose()
}
function Traveler {
    $palette=@{
        K='#222331'; D='#292e49'; N='#3b4c74'; B='#56739a'; L='#89a4bb'
        S='#a76f58'; F='#dfaa7b'; H='#ffe0a4'
        T='#674533'; W='#9e6e43'; G='#d6a366'; A='#a9dacb'; C='#e3fff0'
    }
    $rows=@(
        '.........KKKK...........'
        '.......KKBBNLK..........'
        '......KBBLLBNNK.....KK..'
        '.....KBNBBNNDNK....KWGK.'
        '.....KBNNDDNDSK...KTAHK.'
        '....KNNDDDSFFHK...KWCAK.'
        '....KNDDDSFKKFK....KTK..'
        '....KNDKSFFHFSK....KWK..'
        '.....KDDKSFFSK.....KTK..'
        '....KNBBDDKKK......KWK..'
        '...KBBLNDBNNK......KTK..'
        '...KBNNDBLBBNK.....KWK..'
        '..KNDNDNLBBNNKK....KTK..'
        '..KNDDDNBBNDKFSKK..KWK..'
        '..KNDKDNBDDKFFFSKKGKK...'
        '..KNDKDWGGKNKSSWTWWK...'
        '..KNDKKTWTDNKKKKKKWK...'
        '.KNDKDTWTDDBBK.....KTK..'
        '.KNDKDNNKDLBNK.....KWK..'
        '.KNDKNNK.KNBNK.....KTK..'
        'KNDKDNK..KDNK......KWK..'
        'KDDKDK....KDK......KTK..'
        '.KKKKTK...KTWK.....KWK..'
        '...KWWK...KTWWK....KTK..'
        '...KKKK...KKKKK....KKK..'
    )
    # Keep the silhouettes and material clusters on the logical pixel grid.
    for ($y=0; $y -lt $rows.Count; $y++) {
        for ($x=0; $x -lt $rows[$y].Length; $x++) {
            $key=[string]$rows[$y][$x]
            if ($key -ne '.') { Pixel ($x+4) ($y+3) 1 1 $palette[$key] }
        }
    }
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
        Traveler
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
$ids=@('original','hero')
$labels=@('기존','16비트 전투 도트')
$original=OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$terrain=OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$board=[Drawing.Bitmap]::new(392,332)
$g=[Drawing.Graphics]::FromImage($board)
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
$g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::AntiAliasGridFit
Pixel 0 0 392 332 '#242735'
Label '마법사 주인공 비교' 20 14 24 '#fff0d5'
Label '4배 확대  ·  초원 위 1배' 20 49 14 '#d2c3cb'
for ($i=0; $i -lt 2; $i++) {
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





