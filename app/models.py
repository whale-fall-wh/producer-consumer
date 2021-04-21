# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils import db
from sqlalchemy import func, Table
from sqlalchemy.orm import relationship


class BaseModel(db.Model):
    __abstract__ = True

    def __repr__(self):
        return self.__dict__.__str__()

    def update(self, attributes: dict):
        with db.auto_commit_db():
            if attributes:
                for k, v in attributes.items():
                    setattr(self, k, v)

    @classmethod
    def create(cls, attributes):
        with db.auto_commit_db():
            model = cls(**attributes)
            db.session.add(model)

        return model

    @classmethod
    def update_by_id(cls, model_id: int, data: dict):
        with db.auto_commit_db():
            return db.session.query(cls).filter(cls.id == model_id).update(data)

    @classmethod
    def update_or_create(cls, attributes: dict, values: dict = None):
        with db.auto_commit_db():
            model = db.session.query(cls).filter_by(**attributes).first()
            if model is not None:
                if type(values) == dict:
                    for k, v in values.items():
                        setattr(model, k, v)
            else:
                if type(values) == dict:
                    attributes.update(values)
                model = cls(**attributes)
                db.session.add(model)

            return model

    def delete(self):
        with db.auto_commit_db():
            db.session.delete(self)


class YoutubeUploader(BaseModel):
    __tablename__ = "youtube_uploader"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    uploader_id = db.Column(db.String(32), unique=True, comment="UP主ID")
    uploader = db.Column(db.String(255), index=True, comment="UP主名称")
    uploader_url = db.Column(db.Text, nullable=True, comment="UP主主页")

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    videos = relationship('YoutubeVideo', back_populates="uploader")


class YoutubeVideo(BaseModel):
    __tablename__ = "youtube_video"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(32), unique=True, comment="油管视频ID")
    title = db.Column(db.String(255), comment="油管视频标题")
    description = db.Column(db.Text, nullable=True, comment="描述")
    upload_date = db.Column(db.Date, nullable=True, comment="时间")
    uploader_id = db.Column(db.String(32), db.ForeignKey("youtube_uploader.uploader_id"), index=True, comment="UP主ID")
    channel_id = db.Column(db.String(32), index=True, comment="频道ID", default=0)
    duration = db.Column(db.Integer, comment="时长", default=0)
    view_count = db.Column(db.Integer, comment="播放次数", default=0)
    average_rating = db.Column(db.Float(precision="10,2"), comment="平均评分", default=0.00)
    age_limit = db.Column(db.Integer, comment="年龄限制", default=0)
    like_count = db.Column(db.Integer, comment="喜欢数量", default=0)
    dislike_count = db.Column(db.Integer, comment="不喜欢数量", default=0)
    resource_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey("youtube_resource.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    video_formats = relationship('YoutubeVideoFormat', back_populates="video")
    video_thumbnails = relationship('YoutubeVideoThumbnail', back_populates="video")

    uploader = relationship('YoutubeUploader', back_populates="videos")
    resource = relationship('Resource', uselist=False)


class YoutubeVideoFormat(BaseModel):
    __table_args__ = (db.UniqueConstraint("video_id", "format_id"), )
    __tablename__ = "youtube_video_format"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(32), db.ForeignKey("youtube_video.video_id"), index=True, comment="视频ID")
    format_id = db.Column(db.String(32), index=True)
    asr = db.Column(db.Integer, default=0)
    filesize = db.Column(db.BigInt(unsigned=True), default=0)
    format_note = db.Column(db.String(255), default='')
    fps = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    width = db.Column(db.Integer, nullable=True)
    ext = db.Column(db.String(32), nullable=True)
    quality = db.Column(db.Integer, default=0)
    resource_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey("youtube_resource.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    video = relationship('YoutubeVideo', back_populates="video_formats")
    resource = relationship('Resource', uselist=False)


class YoutubeVideoThumbnail(BaseModel):
    __table_args__ = (db.UniqueConstraint("video_id", "thumbnail_id"),)
    __tablename__ = "youtube_video_thumbnail"
    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(32), db.ForeignKey("youtube_video.video_id"), index=True, comment="视频ID")
    thumbnail_id = db.Column(db.String(32), index=True)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    resolution = db.Column(db.Integer, default=0)
    resource_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey("youtube_resource.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    video = relationship('YoutubeVideo', back_populates="video_thumbnails")
    resource = relationship('Resource', uselist=False)


class Resource(BaseModel):
    __tablename__ = "youtube_resource"
    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, default=1, comment='type=1: 本地图片')
    path = db.Column(db.String(255), default='', comment='本地地址')


if __name__ == '__main__':
    with db.auto_commit_db():
        print(db.session.query(YoutubeUploader).first())
