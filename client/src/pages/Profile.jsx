import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './Profile.css'; 

const Profile = ({ isOwnProfile }) => {
    const { username } = useParams(); 
    const [profile, setProfile] = useState(null);
    const [posts, setPosts] = useState([]); 
    const [error, setError] = useState(null);
    const [isSubscribed, setIsSubscribed] = useState(false);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                let response;
                if (isOwnProfile) {
                    response = await axios.get('http://127.0.0.1:8000/auth/profile', {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                } else {
                    response = await axios.get(`http://127.0.0.1:8000/auth/profile?username=${username}`, {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                }

                setProfile(response.data);

                const userId = response.data.id; 
                const postsResponse = await axios.get(`http://127.0.0.1:8000/post/${userId}/posts/`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });

                setPosts(postsResponse.data); 
            } catch (err) {
                setError('Ошибка при загрузке профиля или постов');
            }
        };

        fetchProfile();
    }, [username, isOwnProfile]);

    const handleSubscribe = async () => {
        try {
            await axios.post(
                'http://127.0.0.1:8000/auth/subscribe', 
                { target_user_id: profile.id }, 
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                }
            );
            setIsSubscribed(true);
        } catch (err) {
            setError('Ошибка при подписке');
        }
    };

    const handleUnsubscribe = async () => {
        try {
            await axios.post(
                'http://127.0.0.1:8000/auth/unsubscribe', 
                { target_user_id: profile.id }, 
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                }
            );
            setIsSubscribed(false);
        } catch (err) {
            setError('Ошибка при отписке');
        }
    };

    if (error) {
        return <div>{error}</div>;
    }

    if (!profile) {
        return <div>Загрузка профиля...</div>;
    }

    return (
        <div className="profile-container">
            <div className="profile-header">
                <div className="profile-photo-placeholder"></div>
                <h1>{profile.name}</h1>
                <p>{profile.email}</p>
                <div className="profile-stats">
                    <span>Подписки: {profile.subscriptions.length}</span>
                    <span>Подписчики: {profile.subscribers.length}</span>
                </div>
            </div>
            {!isOwnProfile && (
                <div className="profile-actions">
                    {isSubscribed ? (
                        <button onClick={handleUnsubscribe} className="unsubscribe-btn">Отписаться</button>
                    ) : (
                        <button onClick={handleSubscribe} className="subscribe-btn">Подписаться</button>
                    )}
                </div>
            )}
            <div className="profile-posts">
                <h2>Посты пользователя:</h2>
                {posts.length === 0 ? (
                    <p>Нет постов для отображения.</p>
                ) : (
                    posts.map(post => (
                        <div key={post.id} className="post">
                            <h3>{post.title}</h3>
                            <p>{post.body}</p>
                            <p><strong>Дата создания:</strong> {new Date(post.created_at).toLocaleDateString()}</p>
                            {post.photos.length > 0 && (
                                <div className="post-photos">
                                    {post.photos.map(photo => (
                                        <img key={photo.id} className="post-images" src={`http://127.0.0.1:8000/${photo.image}`} alt="post" />
                                    ))}
                                </div>
                            )}
                            <div className="post-tags">
                                {post.tags.map(tag => (
                                    <span key={tag.id} className="tag">{tag.name}</span>
                                ))}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default Profile;
