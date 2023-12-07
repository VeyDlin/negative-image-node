from PIL import ImageOps

from invokeai.app.services.image_records.image_records_common import ImageCategory, ResourceOrigin
from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    InputField,
    invocation,
    InvocationContext,
    WithMetadata,
    WithWorkflow,
)

from invokeai.app.invocations.primitives import (
    ImageField,
    ImageOutput
)

@invocation(
    "negative_image",
    title="Negative Image",
    tags=["image", "Negative"],
    category="image",
    version="1.0.0",
)
class NegativeImageInvocation(BaseInvocation, WithMetadata, WithWorkflow):
    """Create negative image from image"""
    image: ImageField = InputField(default=None, description="Input image")

    def invoke(self, context: InvocationContext) -> ImageOutput:
        image = context.services.images.get_pil_image(self.image.image_name)  

        image_dto = context.services.images.create(
            image=ImageOps.invert(image),
            image_origin=ResourceOrigin.INTERNAL,
            image_category=ImageCategory.GENERAL,
            node_id=self.id,
            session_id=context.graph_execution_state_id,
            is_intermediate=self.is_intermediate,
            workflow=self.workflow,
        )

        return ImageOutput(
            image=ImageField(image_name=image_dto.image_name),
            width=image_dto.width,
            height=image_dto.height,
        )
    