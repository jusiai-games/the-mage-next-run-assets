param([Parameter(Mandatory)][string]$Source)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Join-Path $PSScriptRoot '../..'
$portrait=[Drawing.Bitmap]::new($Source)
# Sample the large key pose on a 19 x 26 logical grid, keeping hard pixel edges.
$sprite=[Drawing.Bitmap]::new(32,32)
$colors='#16131b','#35242d','#512c2b','#703832','#92463a','#b45d43','#e68e52','#ffbf77',
        '#613b28','#935930','#c88c4c','#f3be67','#34283f','#4c3c60','#705986','#9275a5',
        '#9f654e','#d29069','#f1b48a','#ffd5a6','#f3e8d8','#38313b','#76656b',
        '#18474b','#287a7c','#4fcac6','#a2f1e4','#edfff5'
$palette=foreach($hex in $colors){[Drawing.ColorTranslator]::FromHtml($hex)}
for($y=0;$y -lt 26;$y++){
    for($x=0;$x -lt 19;$x++){
        $sx=[int][Math]::Floor(24+($x+0.5)*467/19)
        $sy=[int][Math]::Floor(31+($y+0.5)*636/26)
        $sample=$portrait.GetPixel($sx,$sy)
        if($sample.A -lt 128){continue}
        $distance=[double]::PositiveInfinity
        foreach($color in $palette){
            $dr=$sample.R-$color.R; $dg=$sample.G-$color.G; $db=$sample.B-$color.B
            $score=2*$dr*$dr+3*$dg*$dg+2*$db*$db
            if($score -lt $distance){$distance=$score;$chosen=$color}
        }
        $sprite.SetPixel(($x+6),($y+2),$chosen)
    }
}
$portrait.Dispose()
$sprite.Save((Join-Path $PSScriptRoot 'hero-wizard.png'),[Drawing.Imaging.ImageFormat]::Png)
$terrain=[Drawing.Bitmap]::new((Join-Path $root 'exports/v1/meadow-wave-mobile/meadow-terrain.png'))
$original=[Drawing.Bitmap]::new((Join-Path $root 'exports/v1/wizard/idle/hood_staff_idle.png'))
$board=[Drawing.Bitmap]::new(412,285)
$g=[Drawing.Graphics]::FromImage($board)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#313747'))
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
$font=[Drawing.Font]::new('Malgun Gothic',16,[Drawing.GraphicsUnit]::Pixel)
$g.DrawString('기존 스프라이트',$font,[Drawing.Brushes]::White,24,13)
$g.DrawString('첨부 디자인 · 32×32',$font,[Drawing.Brushes]::White,224,13)
$g.DrawImage($original,[Drawing.Rectangle]::new(24,41,160,160),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
$g.DrawImage($sprite,224,41,160,160)
foreach($index in 0..1){
    $x=24+200*$index
    $g.DrawImage($terrain,[Drawing.Rectangle]::new($x,221,160,44),0,50,160,44,[Drawing.GraphicsUnit]::Pixel)
    if($index -eq 0){
        $g.DrawImage($original,[Drawing.Rectangle]::new(($x+64),224,32,32),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
    }else{
        $g.DrawImage($sprite,($x+64),224,32,32)
    }
}
$board.Save((Join-Path $PSScriptRoot 'comparison.png'),[Drawing.Imaging.ImageFormat]::Png)
$font.Dispose()
$g.Dispose()
$board.Dispose()

$sprite.Dispose()
$terrain.Dispose()
$original.Dispose()

