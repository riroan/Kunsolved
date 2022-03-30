import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import MainPage from './components/pages/MainPage'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<MainPage />} />
            </Routes>
        </Router>
    )
}

export default App
