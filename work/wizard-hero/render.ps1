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
function Traveler($variant) {
    $ink='#1c202f'; $dark='#2a3349'; $blue='#3d5678'; $edge='#6284a3'
    # Long cloak, split hem and planted boots.
    Shape $ink @(12,10,19,10,22,13,22,17,20,19,21,24,24,26,20,27,19,28,14,28,14,26,11,28,6,28,6,26,2,26,5,22,7,16)
    Shape $dark @(12,11,18,11,21,14,20,18,18,19,19,25,21,26,16,26,15,23,11,26,8,26,9,24,4,25,7,21,8,16)
    Shape $blue @(10,13,14,12,16,14,14,18,12,22,10,24,5,25,8,20,9,16)
    Shape $edge @(9,15,12,13,13,14,11,17,10,20,7,23,8,20)
    Pixel 7 26 3 1 '#a07a60'
    Pixel 16 26 3 1 '#a07a60'
    Shape '#293f59' @(15,17,18,17,18,22,20,25,17,25,15,21)
    Pixel 13 18 5 1 '#765746'
    Pixel 16 18 2 1 '#d5ac74'
    # Compact hood swept back, with a readable three-quarter face.
    Shape $ink @(7,10,8,6,11,3,15,1,19,2,22,4,23,7,23,11,20,14,15,14,12,12,9,13)
    Shape $blue @(8,10,9,6,12,4,15,2,19,3,21,4,22,7,20,6,17,6,13,8,11,11,9,12)
    Shape $edge @(9,8,10,6,13,4,16,3,19,4,15,5,12,6,11,9,10,10)
    Shape '#bb826b' @(15,8,18,6,21,7,22,10,20,11,20,12,18,13,16,12)
    Shape '#e9b28c' @(17,8,19,7,21,8,21,10,20,12,18,12,17,11)
    Pixel 19 8 2 1 $ink
    Pixel 21 9 1 1 '#ffe0af'
    Pixel 19 11 1 1 '#805957'
    Shape '#45413f' @(13,9,16,6,19,6,18,8,16,9,16,11,14,11)
    Shape $dark @(9,12,12,10,15,12,16,14,13,15,10,14)
    Pixel 12 13 2 1 $edge
    # Unlit hardwood staff with an angular hooked head.
    Shape $ink @(26,28,25,26,26,17,26,11,24,8,24,5,26,2,30,2,32,4,31,7,29,7,28,5,27,6,27,8,29,11,28,18,28,27)
    Shape '#805b47' @(26,26,27,17,27,11,25,8,25,5,27,3,30,3,31,4,30,6,29,5,28,4,26,6,26,8,28,11,27,18,27,26)
    Pixel 27 3 3 1 '#c99d70'
    Pixel 25 6 1 2 '#c99d70'
    Pixel 27 12 2 1 '#beaa89'
    Pixel 27 14 2 1 '#927c63'
    Shape $ink @(17,14,20,12,22,14,25,14,28,15,28,18,24,18,21,18,18,17)
    Shape $blue @(18,14,20,13,22,15,24,15,23,17,20,17,18,16)
    Pixel 19 14 2 1 $edge
    Pixel 25 15 2 2 '#e9b28c'
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
        Traveler $index
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
$labels=@('기존','새 주인공')
$original=OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$terrain=OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$board=[Drawing.Bitmap]::new(392,332)
$g=[Drawing.Graphics]::FromImage($board)
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
$g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::AntiAliasGridFit
Pixel 0 0 392 332 '#242735'
Label '초원을 지키는 후드 마법사' 20 14 24 '#fff0d5'
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

