import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './PostDetail.css';

const PostDetail = () => {
    const { postId } = useParams();
    const [post, setPost] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchPostDetail = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/post/posts/${postId}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                setPost(response.data);
            } catch (err) {
                setError('Ошибка при загрузке поста');
            }
        };

        fetchPostDetail();
    }, [postId]);

    const handleVote = async (voteType) => {
        const url = voteType === 'upvote' 
            ? `http://127.0.0.1:8000/post/${postId}/upvote` 
            : `http://127.0.0.1:8000/post/${postId}/downvote`;

        try {
            await axios.post(url, { post_id: postId }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            setPost(prevPost => ({
                ...prevPost,
                vote_counts: {
                    ...prevPost.vote_counts,
                    [voteType]: (prevPost.vote_counts[voteType] || 0) + 1
                }
            }));
        } catch (err) {
            console.error('Ошибка при голосовании', err);
        }
    };

    const handleAuthorClick = (authorName) => {
        navigate(`/profile/${authorName}`); 
    };

    if (error) {
        return <div>{error}</div>;
    }

    if (!post) {
        return <div>Загрузка поста...</div>;
    }

    return (
        <div className="post-detail">
            <h1>{post.title}</h1>
            <div className="post-header">
                <span className="post-author" onClick={() => handleAuthorClick(post.author_name)}>
                    {post.author_name}
                </span>
                <span className="post-date">{new Date(post.created_at).toLocaleDateString()}</span>
                <span className="post-country">Страна: {post.country_name}</span>
            </div>
            <p>{post.body}</p>
            <div className="post-images">
                {post.photos.map(photo => (
                    <img key={photo.id} src={`http://127.0.0.1:8000/${photo.image}`} alt="Post" />
                ))}
            </div>
            <div className="post-tags">
                {post.tag.map(tag => (
                    <span key={tag.id} className="tag">#{tag.name}</span>
                ))}
            </div>
            <div className="post-actions">
                <button onClick={() => handleVote('upvote')} className="like-btn">👍 {post.vote_counts.upvote || 0}</button>
                <button onClick={() => handleVote('downvote')} className="dislike-btn">👎 {post.vote_counts.downvote || 0}</button>
            </div>
        </div>
    );
};

export default PostDetail;
