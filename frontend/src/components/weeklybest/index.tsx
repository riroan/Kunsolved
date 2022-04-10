import React, { useState, useEffect } from 'react'
import classnames from 'classnames/bind'
import styles from './weeklybest.module.scss'
import { AiFillTrophy } from 'react-icons/ai'
import URL from '../_config/config'
const cx = classnames.bind(styles)

export default function WeeklyBest() {
    const [data, setData] = useState([])

    useEffect(() => {
        const url = `${URL}/weeklyBest`
        console.log(url)
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                setData(res)
            })
    }, [])

    return (
        <div className={cx('main')}>
            <div className={cx('title')}>명예의 전당</div>
            <div className={cx('desc')}>이번주 가장 많은 문제를 푼 사람은 누구?</div>
            <div>(기록은 매주 월요일 초기화됩니다.)</div>
            {data.map((value, i) => {
                return (
                    <a href={`https://www.acmicpc.net/user/${value['name']}`} className={ cx('a')}>
                        <div className={cx(i === 0 ? 'first' : i === 1 ? 'second' : 'third', 'item')}>
                            <AiFillTrophy className={cx('icon')} />
                            <div className={cx('rank')}>{i + 1}</div>
                            <div className={cx('name')}>{value['name']}</div>
                            <div className={cx('cnt')}>{value['cnt']} solved</div>
                        </div>
                    </a>
                )
            })}
        </div>
    )
}
