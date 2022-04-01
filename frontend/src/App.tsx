import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import DetailPage from './components/pages/DetailPage'
import MainPage from './components/pages/MainPage'
import TagDetailPage from './components/pages/TagDetailPage'
import TagPage from './components/pages/TagPage'
import TierPage from './components/pages/TierPage'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/tier" element={<TierPage />} />
                <Route path="/tier/:level" element={<DetailPage />} />
                <Route path="/tag" element={<TagPage />} />
                <Route path="/tag/:name" element={<TagDetailPage />} />
            </Routes>
        </Router>
    )
}

export default App
