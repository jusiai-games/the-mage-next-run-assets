param([Parameter(Mandatory)][string]$Source)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Join-Path $PSScriptRoot '../..'
$portrait=[Drawing.Bitmap]::new($Source)
$bounds=[Drawing.Rectangle]::new(114,83,855,1208)
$large=[Drawing.Bitmap]::new(108,156)
$g=[Drawing.Graphics]::FromImage($large)
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.DrawImage($portrait,[Drawing.Rectangle]::new(0,0,108,156),$bounds,[Drawing.GraphicsUnit]::Pixel)
$g.Dispose()
$portrait.Dispose()
$large.RotateFlip([Drawing.RotateFlipType]::RotateNoneFlipX)
$sprite=[Drawing.Bitmap]::new(32,32)
for ($y=0;$y -lt 26;$y++) {
    for ($x=0;$x -lt 18;$x++) {
        $red=0; $green=0; $blue=0; $count=0
        for($dy=0;$dy -lt 6;$dy++){
            for($dx=0;$dx -lt 6;$dx++){
                $p=$large.GetPixel(($x*6+$dx),($y*6+$dy))
                if([Math]::Max($p.R,[Math]::Max($p.G,$p.B)) -le 11){ continue }
                $red+=$p.R; $green+=$p.G; $blue+=$p.B; $count++
            }
        }
        if($count -lt 17){continue}
        $sprite.SetPixel(($x+7),($y+2),[Drawing.Color]::FromArgb(255,[int]($red/$count),[int]($green/$count),[int]($blue/$count)))
    }
}
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
$g.DrawString('첨부 원화 축소',$font,[Drawing.Brushes]::White,224,13)
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
$large.Dispose()
$sprite.Dispose()
$terrain.Dispose()
$original.Dispose()
