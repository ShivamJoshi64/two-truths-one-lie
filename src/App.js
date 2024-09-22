import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import VideoRecording from './components/VideoRecording';
import AudioRecording from './components/AudioRecording';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/video-recording" element={<VideoRecording />} />
        <Route path="/audio-recording" element={<AudioRecording />} />
      </Routes>
    </Router>
  );
}

export default App;