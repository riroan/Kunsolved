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
            <div className={cx('notice')}>
                <span className={cx('title')}>공지</span>
                <br />
                익명으로 이슈를 받았는데 답장을 남길곳이 없어 여기에 남깁니다.
                <br />
                특정 문제를 해결했는데 처리되지 않은 오류가 있었습니다. 확인해보니 서브태스크 점수가 있는 문제들에 대해서 이런 문제가 발생했습니다.
                <br />
                지금은 해결했으나 이슈가 있었던 2개의 문제는 랭킹 기여와 푼 문제에 기록되지 않을 예정입니다.
                <br />
                이 점 양해해주시기 바랍니다. ㅠㅠ
                <br />
                (이슈 올리신 분 확인하셨으면 기능요청으로 메시지 바랍니다.)
                <br />
                (공지는 자정 지나고 내리겠습니다.)
            </div>
            <Navigation />
            <WeeklyBest />
            <hr />
        </div>
    )
}
