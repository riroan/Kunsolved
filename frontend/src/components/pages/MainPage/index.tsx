import React from 'react'
import Navigation from '../../navigation'
import Menu from '../../menu'
import Header from '../../header'
import WeeklyBest from '../../weeklybest'

export default function MainPage() {
    return (
        <div>
            <Header />
            <Menu />
            <Navigation />
            <WeeklyBest />
            <hr />
        </div>
    )
}
