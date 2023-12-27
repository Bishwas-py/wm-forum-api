from typing import Literal, List

from django.contrib.contenttypes.models import ContentType
from ninja import Router

from posts.models import Post, PolymorphicComments
from posts.schemas import CommentSchema, CreateCommentSchema, PostCreateSchema, LikeSchema

router = Router(tags=["Comments"])

CommentSource = {
    'comment': PolymorphicComments,
    'post': Post
}

CommentTypeLiteral = Literal['comment', 'post']


@router.post("/create/{source_type}/{source_id}", response=CommentSchema, summary="Create a comment on a post")
def create_post_comment(request, source_id: int, source_type: CommentTypeLiteral,
                        data: CreateCommentSchema):
    content_object = CommentSource[source_type].objects.get(id=source_id)
    comment = PolymorphicComments.create_comment(user=request.user, content_object=content_object,
                                                 comment_text=data.comment_text)
    return comment


@router.get("/get/all/{source_type}/{source_id}", response=List[CommentSchema], summary="Get comments on a post")
def get_post_comments(request, source_id: int, source_type: CommentTypeLiteral,
                      belongs_to: bool = False):
    content_object = CommentSource[source_type].objects.get(id=source_id)
    comments = PolymorphicComments.objects.filter(content_type=ContentType.objects.get_for_model(content_object),
                                                  object_id=content_object.id)
    if belongs_to:
        comments = comments.filter(user=request.user)
    return comments
