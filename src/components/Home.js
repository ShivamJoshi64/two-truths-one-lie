import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handleVideo = () => {
    navigate('/video-recording');
  };

  const handleAudio = () => {
    navigate('/audio-recording');
  };

  return (
    <div>
      <h1>2 Truths and 1 Lie</h1>
      <button onClick={handleVideo}>Record Video</button>
      <button onClick={handleAudio}>Use Voice Only</button>
    </div>
  );
};

export default Home;