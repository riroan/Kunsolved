import React, { useState, useEffect } from 'react'
import classnames from 'classnames/bind'
import styles from './weeklybest.module.scss'
import URL from '../_config/config'
const cx = classnames.bind(styles)

export default function WeeklyBest() {
    const [data, setData] = useState([])
    const [contribData, setContribData] = useState([])

    useEffect(() => {
        var url = `${URL}/v1/best/week`
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
        url = `${URL}/v1/best/contrib`
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                setContribData(res)
            })
    }, [])

    return (
        <div className={cx('main')}>
            <div className={cx('title')}>명예의 전당</div>
            <div className={cx('desc')}>(기록은 매주 월요일 초기화됩니다.)</div>
            <div className={cx('rank-wrapper')}>
                <div className={cx('solved-rank')}>
                    <div className={cx('rank-title')}>푼 문제</div>
                {data.map((value, i) => {
                          return (
                              <a href={`https://www.acmicpc.net/user/${value['name']}`} className={cx('a')} key={i}>
                                  <div className={cx(i === 0 ? 'first' : i <= 3 ? 'second' : 'third', 'item')}>
                                      <div className={cx('rank')}>#{i + 1}</div>
                                      <div className={cx('name')}>{value['name']}</div>
                                      <div className={cx('cnt')}>{value['cnt']}</div>
                                  </div>
                              </a>
                      )
                  })
                }
                </div>
                <div className={cx('distribution-rank')}>
                    <div className={cx('rank-title')}>학교 랭킹 기여</div>
                    {contribData.map((value, i) => {
                        return (
                            <a href={`https://www.acmicpc.net/user/${value['name']}`} className={cx('a')} key={i}>
                                <div className={cx(i === 0 ? 'first' : i <= 3 ? 'second' : 'third', 'item')}>
                                    <div className={cx('rank')}>#{i + 1}</div>
                                    <div className={cx('name')}>{value['name']}</div>
                                    <div className={cx('cnt')}>{value['cnt']}</div>
                                </div>
                            </a>
                        )
                    })
                    }
                </div>
            </div>
        </div>
    )
}
