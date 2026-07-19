# tiny-lora-v1 stats

Total examples: **74**

| tag | count |
|---|---|
| `contour_allow_client` | 9 |
| `contour_clarify` | 13 |
| `contour_refuse_public` | 10 |
| `format_bullets` | 7 |
| `format_sentences` | 14 |
| `format_short` | 3 |
| `general_ru` | 12 |
| `json_code` | 6 |

## v1 extras focus

- `contour_clarify` — ambiguous «облако» → ask public vs private (never bare Нет)
- `format_sentences` — more exactly-2-sentence formal prompts
- `general_ru` — richer 3–5 sentence air-gap answers
- `contour_allow_client` — longer VPC/allowlist detail

File: `datasets/tiny-lora-v1/train.messages.jsonl`
