from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

videos_put_args = reqparse.RequestParser()
videos_put_args.add_argument("name",type=str, help="Name of the video", required=True)
videos_put_args.add_argument("views",type=int, help="Views of the video", required=True)
videos_put_args.add_argument("likes",type=int, help="Likes of the video", required=True)

videos_update_args = reqparse.RequestParser()
videos_update_args.add_argument("name",type=str, help="Name of the video")
videos_update_args.add_argument("views",type=int, help="Views of the video")
videos_update_args.add_argument("likes",type=int, help="Likes of the video")


resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,videos_id):
        result = VideoModel.query.filter_by(id=videos_id).first()
        if(not result):
            abort(404,message = "Can't find video with that id")
        return result

    @marshal_with(resource_fields)
    def put(self,videos_id):
        args = videos_put_args.parse_args()
        result = VideoModel.query.filter_by(id=videos_id).first()
        if (result):
            abort(409,message = "Video id taken")
        video = VideoModel(id=videos_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, videos_id):
        args =  videos_update_args.parse_args()
        result = VideoModel.query.filter_by(id=videos_id).first()
        if (not result):
            abort(404,message = "Video doesn't exist can't update")
        
        if(args['name']):
            result.name = args['name']
        if(args['views']):
            result.views = args['views']
        if(args['likes']):
            result.likes = args['likes']
        
        db.session.commit()

        return result

    @marshal_with(resource_fields)
    def delete(self,videos_id):
        del videos[videos_id]
        return '',204

api.add_resource(Video, "/video/<int:videos_id>")

if __name__ =="__main__":
    app.run(debug=True)