from ..models import Stage
from . import stage1_basics, stage2_pipes, stage3_transform, stage4_advanced, stage5_expert


def load_all() -> list[Stage]:
    return [
        stage1_basics.STAGE,
        stage2_pipes.STAGE,
        stage3_transform.STAGE,
        stage4_advanced.STAGE,
        stage5_expert.STAGE,
    ]
