# 7B VPC pack — one remaining contour hole

After holes LoRA (`15/20` / `19/20`) the leftover id is `contour_allow_client`:
the model allows VPC but invents a public **API Gateway**.

This pack: VPC/private cloud is allowed; API listens on an **internal** address;
**no** API Gateway, **no** public ingress, **no** required internet egress.

Anchors keep ids that already score 2. Resume `artifacts/runs/20260813-mlx-7b-holes/adapter`.
