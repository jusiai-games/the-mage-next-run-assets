using UnityEngine;

[DisallowMultipleComponent]
public sealed class StageSlimeHop : MonoBehaviour
{
    [SerializeField] private SpriteRenderer slime = null;
    [SerializeField] private Sprite[] frames = new Sprite[0];

    private static readonly int[] FrameMilliseconds = {
        40, 30, 30, 20, 30, 30, 30, 30, 30,
        30, 30, 30, 30, 30, 30, 30, 30, 30,
    };
    private const int LoopMilliseconds = 540;
    private float elapsedMilliseconds;

    private void OnEnable()
    {
        elapsedMilliseconds = 0;
        ApplyFrame();
    }

    private void Update()
    {
        elapsedMilliseconds = Mathf.Repeat(elapsedMilliseconds + 1000f * Time.unscaledDeltaTime,
            LoopMilliseconds);
        ApplyFrame();
    }

    private void ApplyFrame()
    {
        if (slime == null || frames.Length != FrameMilliseconds.Length)
            return;

        float time = elapsedMilliseconds;
        for (int index = 0; index < frames.Length; index++)
        {
            time -= FrameMilliseconds[index];
            if (time < 0f)
            {
                slime.sprite = frames[index];
                return;
            }
        }
    }
}
