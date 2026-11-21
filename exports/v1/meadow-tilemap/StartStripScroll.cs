using UnityEngine;

[DisallowMultipleComponent]
public sealed class StartStripScroll : MonoBehaviour
{
    [SerializeField] private SpriteRenderer primary = null;
    [SerializeField] private SpriteRenderer repeat = null;
    [SerializeField] private float pixelsPerSecond = 10f;

    private Vector3 origin;
    private Vector3 repeatOrigin;
    private float pixelOffset;
    private bool initialized;

    private void OnEnable()
    {
        if (primary == null || repeat == null || primary.sprite == null ||
            primary.transform.parent != repeat.transform.parent)
            return;

        origin = primary.transform.localPosition;
        repeatOrigin = repeat.transform.localPosition;
        pixelOffset = 0f;
        initialized = true;
        ApplyOffset();
    }

    private void Update()
    {
        if (!initialized)
            return;

        pixelOffset = Mathf.Repeat(pixelOffset + pixelsPerSecond * Time.unscaledDeltaTime,
            primary.sprite.rect.width);
        ApplyOffset();
    }

    private void ApplyOffset()
    {
        float width = primary.sprite.rect.width;
        float ppu = primary.sprite.pixelsPerUnit;
        float xScale = primary.transform.localScale.x;
        float pixel = Mathf.Round(pixelOffset) % width;
        primary.transform.localPosition = origin + Vector3.left * (pixel * xScale / ppu);
        repeat.transform.localPosition = origin + Vector3.right * ((width - pixel) * xScale / ppu);
    }

    private void OnDisable()
    {
        if (!initialized)
            return;

        primary.transform.localPosition = origin;
        repeat.transform.localPosition = repeatOrigin;
        initialized = false;
    }
}
