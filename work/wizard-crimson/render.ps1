$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$out = $PSScriptRoot
$root = Join-Path $out '../..'
function Pixel($x,$y,$w,$h,$color) {
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.FillRectangle($brush,[int]$x,[int]$y,[int]$w,[int]$h)
    $brush.Dispose()
}
function Shape($color,[int[]]$coords) {
    [Drawing.Point[]]$points = for ($i=0; $i -lt $coords.Count; $i+=2) {
        [Drawing.Point]::new($coords[$i],$coords[$i+1])
    }
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.FillPolygon($brush,$points)
    $brush.Dispose()
}
function Traveler {
    $ink='#272030'; $red='#a03646'; $redLight='#d45a50'; $wine='#612c43'
    $ivory='#f2d7a5'; $gold='#d49a57'; $skin='#e6a578'
    # Split red coat swept away from the direction of the cast.
    Shape $ink @(10,10,17,9,22,12,21,17,18,19,19,23,13,25,8,24,3,27,0,25,3,21,4,17,8,15)
    Shape $wine @(10,11,17,10,20,12,19,17,16,20,17,22,13,24,8,23,3,26,1,25,4,21,5,17,9,16)
    Shape $red @(9,15,13,15,12,18,10,21,6,22,3,25,2,25,5,20,6,17)
    Shape $redLight @(6,18,10,16,12,16,10,18,7,20,5,21)
    # Bent legs and boots planted far apart.
    Shape $ink @(11,16,18,16,19,19,23,20,24,24,26,26,26,28,20,28,19,25,18,22,15,22,13,24,11,26,11,28,5,28,5,26,8,24,9,20)
    Shape '#46394c' @(12,17,17,17,18,20,22,21,23,24,20,25,19,22,15,21,12,24,10,25,8,25,10,21)
    Shape '#756077' @(17,20,21,21,22,23,20,23,19,22)
    Pixel 6 26 4 1 '#a47a65'
    Pixel 21 26 3 1 '#a47a65'
    # Cropped jacket, folded cream lapel and extended sleeve.
    Shape $ink @(10,10,16,9,20,11,22,11,25,9,27,10,26,13,23,15,20,15,18,18,11,19,9,16)
    Shape $red @(11,11,16,10,19,12,22,12,25,10,26,11,24,13,21,14,19,13,17,17,12,18,10,16)
    Shape $ivory @(13,11,16,10,18,11,16,14,14,16,12,15,14,13)
    Pixel 15 16 2 1 $gold
    Pixel 12 17 5 1 '#754844'
    Shape $redLight @(19,12,22,12,24,11,23,13,20,14)
    # Angular profile and a swept cream-colored forelock.
    Shape $ink @(9,9,8,6,8,3,11,3,13,1,17,1,20,2,21,4,20,6,21,7,21,9,18,10,17,12,13,12,11,10)
    Shape '#8b776b' @(9,6,9,4,12,4,14,2,18,2,20,3,19,5,16,5,14,8,12,9)
    Shape $ivory @(10,5,13,4,15,2,18,2,19,3,16,4,15,5,12,6,11,7)
    Pixel 14 3 3 1 '#fff0cb'
    Shape '#a76c5c' @(13,8,15,6,19,5,19,7,21,8,19,9,18,11,15,11)
    Shape $skin @(15,8,17,6,19,6,19,8,20,8,18,10,16,10)
    Pixel 17 7 2 1 $ink
    Pixel 18 9 1 1 '#975850'
    # Staff runs from the low back hand to a compact metal head.
    Shape $ink @(6,21,5,20,7,18,24,8,26,5,29,3,31,4,32,6,30,8,27,9,9,20)
    Shape '#7f5146' @(7,20,7,19,25,8,27,7,27,8,9,19)
    Shape $gold @(25,8,27,5,29,4,31,5,31,6,29,7,27,8)
    Pixel 29 5 2 1 '#8ee0ce'
    Pixel 29 5 1 1 '#e5fff0'
    Shape $ink @(21,11,24,10,27,10,28,12,25,14,22,14)
    Shape $skin @(22,11,26,11,26,12,24,13,22,13)
    Pixel 24 11 2 1 $ivory
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
$labels=@('기존','진홍 코트 마법사')
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




