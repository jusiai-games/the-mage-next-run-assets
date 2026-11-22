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
function Wizard($design) {
    $ink='#24222c'
    switch ($design) {
        1 { $deep='#49313a'; $mid='#804345'; $lit='#ba6350'; $glow='#ffad56'; $core='#fff1aa' }
        2 { $deep='#243d54'; $mid='#355d78'; $lit='#668ca0'; $glow='#57dfea'; $core='#d8ffff' }
        3 { $deep='#3f3657'; $mid='#65577a'; $lit='#93859c'; $glow='#e6bb65'; $core='#fff0b5' }
    }
    Shape $ink @(10,10,18,9,22,13,22,19,20,22,22,27,20,28,15,28,14,25,12,28,7,28,7,26,2,27,4,23,5,17)
    Shape $deep @(10,12,17,11,20,14,20,19,18,22,20,26,16,26,14,23,11,26,8,26,9,23,4,25,6,20)
    Shape $mid @(8,15,13,13,15,16,13,21,6,24,8,20)
    Shape $lit @(9,16,12,15,11,19,8,22)
    Pixel 8 26 3 1 $lit
    Pixel 17 26 3 1 $lit
    Shape $ink @(12,12,18,11,22,14,23,17,26,17,25,21,20,21,17,18,13,19)
    Shape $lit @(14,13,18,12,21,15,18,17,14,17)
    Pixel 14 17 4 2 $mid
    Pixel 16 21 3 1 $lit
    Pixel 17 21 1 1 $glow
    switch ($design) {
        1 {
            Shape $ink @(6,10,10,8,11,5,15,2,19,3,21,8,24,9,25,11,21,13,9,13,5,12)
            Shape $mid @(7,11,11,9,12,6,16,3,19,4,20,8,22,10,18,11,10,12)
            Shape $lit @(12,9,13,6,16,4,18,4,16,6,15,8)
            Pixel 16 10 5 1 $glow
            Pixel 18 12 3 2 '#c78a68'
            Shape $mid @(10,14,15,14,18,16,17,18,12,17,8,18)
            Shape $ink @(25,7,27,7,28,14,27,26,25,28,24,27,25,18)
            Pixel 26 12 1 13 '#ac795e'
            Shape $ink @(24,4,27,2,30,4,31,8,28,12,25,11,23,8)
            Shape $lit @(25,5,27,4,30,6,29,9,27,11,25,9)
            Pixel 27 5 2 3 $glow
            Pixel 28 5 1 2 $core
        }
        2 {
            Shape $ink @(9,12,8,8,10,4,13,2,18,2,22,5,23,9,20,12,16,12,14,15,10,15)
            Shape $mid @(10,11,9,8,11,5,14,3,18,3,21,5,22,8,17,8,14,11,13,14,11,14)
            Shape $lit @(10,8,12,5,15,4,19,4,16,5,13,7,12,10)
            Pixel 17 9 4 1 $glow
            Pixel 18 10 3 2 '#b39379'
            Shape $ink @(23,26,25,11,23,8,24,3,26,2,26,7,28,8,29,6,29,3,31,4,31,9,28,12,26,27)
            Pixel 25 4 1 4 $lit
            Pixel 30 5 1 4 $lit
            Pixel 27 6 1 4 $glow
            Pixel 27 8 2 1 $core
            Shape $lit @(26,12,27,12,25,25,24,26)
        }
        3 {
            Shape $ink @(8,13,8,8,11,4,16,2,20,3,23,7,23,11,21,14,17,15,13,12,11,16,8,16)
            Shape $mid @(9,12,9,8,12,5,16,3,20,4,22,7,22,10,18,8,14,10,11,13,10,15,9,15)
            Shape $lit @(10,9,12,6,16,4,19,4,16,6,12,9,10,13)
            Shape '#b39970' @(16,10,21,9,22,11,20,14,18,14,16,12)
            Pixel 19 10 2 1 $core
            Shape $ink @(24,27,24,20,26,11,24,8,24,5,27,2,30,4,32,7,29,11,27,15,26,27)
            Shape $glow @(25,6,27,3,30,5,31,7,28,10,25,8)
            Shape $deep @(26,6,28,5,30,7,28,9,26,8)
            Pixel 27 6 1 2 $core
            Shape $lit @(27,12,28,12,25,26,25,22)
        }
    }
    Pixel 22 17 3 2 $lit
    Pixel 22 19 2 1 $mid
}

function Slime($design) {
    switch ($design) {
        1 {
            $ink='#342732'; $deep='#62353b'; $mid='#a84b3d'; $light='#dc7649'; $glow='#ffbf62'
            Shape $ink @(3,24,5,20,8,19,10,15,13,15,15,11,19,13,20,16,24,16,25,20,29,22,30,25,27,28,7,28)
            Shape $deep @(4,24,6,21,10,20,11,16,14,17,16,13,19,15,20,18,23,17,25,21,28,23,29,25,26,27,7,27)
            Shape $mid @(5,24,9,21,12,20,13,17,15,18,17,14,19,17,20,20,24,19,25,23,28,24,25,26,10,26)
            Shape $light @(14,20,17,17,21,20,23,22,19,25,15,25,13,23)
            Shape $glow @(15,21,18,19,21,21,21,23,18,24,15,23)
            Pixel 18 21 2 2 '#fff0a6'
            Pixel 7 24 4 1 $light
        }
        2 {
            $ink='#233748'; $deep='#2c5666'; $mid='#367e89'; $light='#63b6b2'; $glow='#bcffda'
            Shape $ink @(3,24,5,20,9,18,12,15,15,14,17,10,19,11,18,15,21,15,25,13,26,15,23,19,27,21,29,24,27,27,23,28,7,28)
            Shape $deep @(4,24,6,21,10,19,13,16,16,15,18,11,18,16,21,16,25,14,24,17,22,19,26,22,28,24,26,26,22,27,7,27)
            Shape $mid @(6,24,7,21,12,19,15,16,18,16,17,19,23,19,26,23,26,25,21,26,8,26)
            Shape $light @(7,22,11,20,14,17,17,17,16,20,20,20,18,23,12,23,9,25)
            Shape $glow @(17,14,16,19,20,18,16,24,17,20,14,21)
        }
        3 {
            $ink='#2c2939'; $deep='#443a59'; $mid='#69577d'; $light='#9b83a9'; $glow='#efc275'
            Shape $ink @(2,24,5,20,8,18,10,13,13,14,15,16,18,10,22,12,23,17,26,15,29,18,28,21,31,24,28,27,24,28,6,28)
            Shape $deep @(4,24,6,21,9,19,11,14,14,17,16,18,19,11,21,13,22,19,26,16,28,18,27,22,29,24,27,26,23,27,7,27)
            Shape $mid @(6,24,9,21,11,16,14,19,16,20,19,13,21,16,21,21,25,18,27,19,25,23,28,24,24,26,8,26)
            Shape $light @(11,16,13,19,12,22,9,23)
            Shape $light @(19,13,20,14,19,19,17,21)
            Pixel 21 23 4 1 $mid
        }
    }
    Shape $ink @(6,20,10,22,11,24,7,23)
    Shape $ink @(11,23,15,20,15,23,12,25)
    Pixel 8 22 1 1 $glow
    Pixel 13 22 1 1 $glow
}
function OpenBitmap($path) { [Drawing.Bitmap]::new((Join-Path $root $path)) }
$terrain = OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$oldWizard = OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$oldSlime = OpenBitmap 'exports/v1/meadow-slime/idle/slime32_idle.png'
$board = [Drawing.Bitmap]::new(756,480)
$entries = @(
    @{ Label='기존'; Wizard='후드 마법사'; Slime='초원 슬라임' },
    @{ Label='A'; Wizard='잿불 추적자'; Slime='용암핵 슬라임' },
    @{ Label='B'; Wizard='폭풍 전투마법사'; Slime='전격 슬라임' },
    @{ Label='C'; Wizard='봉인 집행관'; Slime='흑요석 슬라임' }
)
function Text($value,$x,$y,$size,$color) {
    $font = [Drawing.Font]::new('Malgun Gothic',$size,[Drawing.GraphicsUnit]::Pixel)
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.DrawString($value,$font,$brush,[single]$x,[single]$y)
    $font.Dispose()
    $brush.Dispose()
}
function Sprite($kind,$design,$old) {
    $sprite = [Drawing.Bitmap]::new(32,32)
    $g = [Drawing.Graphics]::FromImage($sprite)
    if ($design -eq 0) {
        $g.DrawImage($old,[Drawing.Rectangle]::new(0,0,32,32),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
    } else {
        if ($kind -eq 'wizard') { Wizard $design } else { Slime $design }
        $prefix = $entries[$design].Label.ToLowerInvariant()
        $sprite.Save((Join-Path $out "$prefix-$kind.png"),[Drawing.Imaging.ImageFormat]::Png)
        for ($x=0; $x -lt 32; $x++) {
            for ($y=0; $y -lt 32; $y++) {
                $alpha = $sprite.GetPixel($x,$y).A
                if ($alpha -notin @(0,255) -or ($alpha -gt 0 -and $y -ge 28)) { throw "Invalid sprite pixel at $x,$y" }
            }
        }
    }
    $g.Dispose()
    $sprite
}
$g = [Drawing.Graphics]::FromImage($board)
$g.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode = [Drawing.Drawing2D.PixelOffsetMode]::Half
$g.TextRenderingHint = [Drawing.Text.TextRenderingHint]::AntiAliasGridFit
Pixel 0 0 756 480 '#242332'
Text '마법사와 초원 슬라임' 20 14 24 '#fff0d5'
Text '대기 포즈  ·  최근접 4배 확대와 초원 1배 비교' 21 48 14 '#c6b6c7'
for ($i=0; $i -lt 4; $i++) {
    $x = 18+182*$i
    $wizard = Sprite 'wizard' $i $oldWizard
    $slime = Sprite 'slime' $i $oldSlime
    $entry = $entries[$i]
    Pixel $x 80 174 382 '#333143'
    Text $entry.Label ($x+12) 87 17 '#ffdc9e'
    Pixel ($x+8) 112 158 132 '#454257'
    $g.DrawImage($wizard,[Drawing.Rectangle]::new(($x+23),114,128,128))
    Text $entry.Wizard ($x+10) 248 14 '#fff0d5'
    Pixel ($x+8) 273 158 110 '#454257'
    $g.DrawImage($slime,[Drawing.Rectangle]::new(($x+23),269,128,128))
    Text $entry.Slime ($x+10) 388 14 '#fff0d5'
    $g.DrawImage($terrain,[Drawing.Rectangle]::new(($x+7),410,160,42),0,50,160,42,[Drawing.GraphicsUnit]::Pixel)
    $g.DrawImage($wizard,($x+15),411,32,32)
    $g.DrawImage($slime,($x+105),411,32,32)
    $wizard.Dispose()
    $slime.Dispose()
}
$board.Save((Join-Path $out 'comparison.png'),[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$board.Dispose()
$terrain.Dispose()
$oldWizard.Dispose()
$oldSlime.Dispose()

