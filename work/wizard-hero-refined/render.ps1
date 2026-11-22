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
    $ink='#1d2330'; $deep='#28344b'; $blue='#405978'; $edge='#6e8da4'
    # Cape sweeps behind the torso, leaving both legs readable.
    Shape $ink @(10,9,17,9,19,12,17,17,15,20,13,24,9,26,3,26,1,24,5,23,7,19,7,14)
    Shape $deep @(10,10,16,10,17,13,15,17,13,21,11,24,8,25,3,25,6,23,8,19,8,14)
    Shape $blue @(10,11,13,10,14,13,12,15,10,19,8,22,5,24,7,21,9,17,9,13)
    Pixel 9 13 2 1 $edge
    Pixel 8 23 2 1 '#4b657f'
    # Long coat over tapered trousers and sturdy boots.
    Shape $ink @(13,9,18,8,21,10,22,14,20,17,20,21,22,24,22,26,24,26,24,28,18,28,17,25,15,21,14,24,13,27,12,28,7,28,7,26,10,25,11,20,12,16)
    Shape $deep @(14,10,18,9,20,11,20,15,18,18,19,22,21,25,19,26,17,23,15,19,14,20,13,24,11,26,10,26,12,21,12,17)
    Shape $blue @(16,10,18,10,19,12,18,14,16,15,15,18,13,21,13,17,14,13)
    Shape '#576a83' @(18,19,19,21,20,23,19,24,17,22,17,20)
    Pixel 13 17 6 1 '#5e4c47'
    Pixel 16 17 2 1 '#bc946b'
    Pixel 8 26 4 1 '#826954'
    Pixel 19 26 3 1 '#826954'
    # Fitted hood turned back in the wind. Two pixels define the gaze.
    Shape $ink @(10,7,11,4,14,2,18,1,21,2,22,4,23,6,22,9,20,11,15,11,13,9,9,10)
    Shape $blue @(11,7,12,4,15,3,18,2,21,3,22,5,19,4,16,5,14,7,12,8,10,9)
    Shape $edge @(12,5,15,3,18,2,20,3,17,3,15,4,13,6)
    Shape '#bb826d' @(16,6,19,4,21,5,21,7,23,7,22,8,21,8,21,10,18,10,16,8)
    Shape '#ebba94' @(18,6,20,5,21,6,21,8,20,9,18,9)
    Pixel 19 6 2 1 $ink
    Pixel 20 8 1 1 '#915951'
    Shape '#594243' @(15,6,17,4,20,4,19,5,17,6,16,8,15,8)
    Pixel 15 10 4 1 $edge
    # Slim, scorched ash staff. A carved slit catches the light.
    Shape $ink @(26,28,25,27,26,16,26,7,25,5,26,3,28,1,30,1,31,3,29,5,29,12,28,22,28,28)
    Shape '#795d50' @(26,27,27,16,27,7,26,5,27,3,29,2,30,2,29,4,28,6,28,12,27,26)
    Pixel 28 3 1 2 '#dcc299'
    Pixel 27 10 1 2 '#b89d7b'
    # Bent forearm and gloved grip.
    Shape $ink @(18,11,21,10,22,13,24,14,26,13,29,13,29,16,26,17,23,17,20,16)
    Shape $blue @(19,12,21,11,21,14,24,15,25,14,26,15,24,16,22,16,20,15)
    Pixel 19 12 2 1 $edge
    Pixel 26 14 2 2 '#9d765f'
    Pixel 27 14 1 1 '#e0ab84'
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
$labels=@('기존','수정 시안')
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


