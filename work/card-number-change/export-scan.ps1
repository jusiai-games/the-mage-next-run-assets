$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$out=Join-Path $PSScriptRoot '../../exports/v1/wood-spell-cards/number-change'
New-Item -ItemType Directory -Force $out | Out-Null
$art=@{mask=[Drawing.Bitmap]::new(192,36); overlay=[Drawing.Bitmap]::new(192,36)}
foreach($layer in $art.Keys){
    $g=[Drawing.Graphics]::FromImage($art[$layer])
    for($f=0;$f -lt 16;$f++){
        $x=($f%8)*24
        $y=[int][math]::Floor($f/8)*18
        $scan=[math]::Min(24,[math]::Max(0,($f-1)*3))
        if($layer -eq 'mask'){
            if($scan -lt 24){Rect ($x+$scan) $y (24-$scan) 18 '#ffffff'}
            continue
        }
        if($f -ge 1 -and $f -le 8){
            Rect ($x+$scan) ($y+2) 1 14 '#fff2b4'
            if($scan -gt 0){Rect ($x+$scan-1) ($y+3) 1 12 '#d87249'}
            Rect ($x+$scan) ($y+2) 2 1 '#ffc170'
            Rect ($x+$scan) ($y+15) 2 1 '#ffc170'
        }
        for($k=0;$k -lt 8;$k++){
            $age=$f-(2+$k)
            if($age -lt 0 -or $age -gt 4){continue}
            $px=$x+[math]::Max(0,2+$k*2-$age)
            $py=$y+[math]::Max(0,6+($k*7)%8-$age)
            $ink=if($age -lt 2){'#fff2ac'}elseif($age -lt 4){'#ffae5d'}else{'#c25a41'}
            Rect $px $py 1 1 $ink
        }
    }
    $g.Dispose()
    $bitmap=$art[$layer]
    for($py=0;$py -lt $bitmap.Height;$py++){
        for($px=0;$px -lt $bitmap.Width;$px++){
            $alpha=$bitmap.GetPixel($px,$py).A
            if($alpha -notin 0,255){throw "Invalid transparency: $layer"}
            if($py -ge 18 -and $px -ge 168 -and $alpha -ne 0){throw "Final frame is not empty: $layer"}
        }
    }
    $bitmap.Save((Join-Path $out "scan-$layer.png"),[Drawing.Imaging.ImageFormat]::Png)
    $bitmap.Dispose()
}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'flame-transfer.gif') -Destination (Join-Path $out 'preview.gif')
