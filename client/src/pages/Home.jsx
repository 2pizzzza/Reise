import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // для перенаправления
import './Home.css'; // Стили для главной страницы

const Home = () => {
    const [posts, setPosts] = useState([]);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // используем для навигации на профиль

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/post/posts/', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                setPosts(response.data);
            } catch (err) {
                setError('Ошибка при загрузке постов');
            }
        };

        fetchPosts();
    }, []);

    const handleAuthorClick = (authorName) => {
        navigate(`/profile/${authorName}`); // Переход на страницу профиля
    };

    if (error) {
        return <div>{error}</div>;
    }

    if (!posts.length) {
        return <div>Загрузка постов...</div>;
    }

    return (
        <div className="posts-container">
            {posts.map(post => (
                <div className="post" key={post.id}>
                    <div className="post-header">
                        <span className="post-author" onClick={() => handleAuthorClick(post.author.name)}>
                            {post.author.name}
                        </span>
                        <span className="post-date">{new Date(post.created_at).toLocaleDateString()}</span>
                    </div>
                    <h3>{post.title}</h3>
                    <p>{post.body}</p>
                    <div className="post-images">
                        {post.photos.map(photo => (
                            <img key={photo.id} src={`http://127.0.0.1:8000/${photo.image}`} alt="Post" />
                        ))}
                    </div>
                    <div className="post-tags">
                        {post.tags.map(tag => (
                            <span key={tag.id} className="tag">#{tag.name}</span>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Home;
