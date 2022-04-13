import React from 'react'
import Navigation from '../../navigation'
import Menu from '../../menu'
import Header from '../../header'
import WeeklyBest from '../../weeklybest'
import styles from './MainPage.module.scss'
import classnames from 'classnames/bind'
const cx = classnames.bind(styles)

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
