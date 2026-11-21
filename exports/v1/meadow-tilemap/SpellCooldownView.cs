using UnityEngine;

[DisallowMultipleComponent]
public sealed class SpellCooldownView : MonoBehaviour
{
    [SerializeField] private SpriteRenderer spellFace = null;
    [SerializeField] private SpriteRenderer chargeFace = null;
    [SerializeField] private SpriteRenderer chargeEdge = null;
    [SerializeField] private SpriteRenderer readyRim = null;

    private static readonly Color32 DimTint = new Color32(64, 64, 64, 255);
    private Sprite cachedSource;
    private Sprite[] chargeRows;
    private float duration;
    private float elapsed;

    public bool IsReady => elapsed >= duration;
    public float Progress => duration > 0f ? elapsed / duration : 1f;

    // Call after the gameplay code confirms a cast.
    public bool TryStartCooldown(float seconds)
    {
        if (!IsReady || seconds <= 0f || float.IsNaN(seconds) || float.IsInfinity(seconds))
            return false;

        duration = seconds;
        elapsed = 0f;
        ApplyFill();
        return true;
    }

    private void OnEnable()
    {
        ApplyFill();
    }

    private void Update()
    {
        if (IsReady)
            return;

        elapsed = Mathf.Min(duration, elapsed + Time.deltaTime);
        ApplyFill();
    }

    private void ApplyFill()
    {
        if (readyRim != null)
            readyRim.enabled = IsReady;

        if (spellFace != null)
            spellFace.color = IsReady ? Color.white : (Color)DimTint;

        Sprite source = spellFace != null ? spellFace.sprite : null;
        int rows = source != null ? Mathf.RoundToInt(source.rect.height) : 0;
        int revealed = Mathf.Clamp(Mathf.FloorToInt(rows * Progress + 0.5f), 0, rows);
        bool showCharge = !IsReady && revealed > 0 && chargeFace != null && !source.packed;
        if (chargeFace != null)
            chargeFace.enabled = showCharge;
        if (chargeEdge != null)
            chargeEdge.enabled = showCharge;
        if (!showCharge)
            return;

        if (source != cachedSource)
        {
            ReleaseSprites();
            cachedSource = source;
            chargeRows = new Sprite[rows + 1];
        }

        if (chargeRows[revealed] == null)
        {
            Rect crop = source.rect;
            crop.height = revealed;
            chargeRows[revealed] = Sprite.Create(source.texture, crop, Vector2.zero,
                source.pixelsPerUnit, 0, SpriteMeshType.FullRect);
        }

        float ppu = source.pixelsPerUnit;
        float bottom = -source.pivot.y / ppu;
        chargeFace.sprite = chargeRows[revealed];
        chargeFace.color = Color.white;
        chargeFace.transform.localPosition = new Vector3(-source.pivot.x / ppu, bottom, 0);

        if (chargeEdge != null)
        {
            float center = (source.rect.width * 0.5f - source.pivot.x) / ppu;
            chargeEdge.transform.localPosition = new Vector3(center, bottom + (revealed - 0.5f) / ppu, 0);
        }
    }

    private void OnDestroy()
    {
        ReleaseSprites();
    }

    private void ReleaseSprites()
    {
        if (chargeRows == null)
            return;

        foreach (Sprite sprite in chargeRows)
        {
            if (sprite != null)
                Destroy(sprite);
        }

        chargeRows = null;
    }
}
