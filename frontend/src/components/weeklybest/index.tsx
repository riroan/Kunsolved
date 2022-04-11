import React, { useState, useEffect } from 'react'
import classnames from 'classnames/bind'
import styles from './weeklybest.module.scss'
import { AiFillTrophy } from 'react-icons/ai'
import URL from '../_config/config'
const cx = classnames.bind(styles)

export default function WeeklyBest() {
    const [data, setData] = useState([])
    const [contribData, setContribData] = useState([])
    const [feat, setFeat] = useState(false)

    useEffect(() => {
        var url = `${URL}/weeklyBest`
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
        url = `${URL}/contribBest`
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
                console.log(res)
            })
    }, [])

    return (
        <div className={cx('main')}>
            <div className={cx('title')}>명예의 전당</div>
            <div className={cx('desc')}>(기록은 매주 월요일 초기화됩니다.)</div>
            <div className={ cx('buttonSet')}>
                <button
                    className={cx(!feat && 'selected', 'button')}
                    onClick={() => {
                        setFeat(false)
                    }}
                >
                    푼 문제
                </button>
                <button
                    className={cx(feat && 'selected', 'button')}
                    onClick={() => {
                        setFeat(true)
                    }}
                >
                    랭킹 기여
                </button>
            </div>
            {feat
                ? contribData.map((value, i) => {
                      return (
                          <a href={`https://www.acmicpc.net/user/${value['name']}`} className={cx('a')} key={i}>
                              <div className={cx(i === 0 ? 'first' : i <= 3 ? 'second' : 'third', 'item')}>
                                  <AiFillTrophy className={cx('icon')} />
                                  <div className={cx('rank')}>{i + 1}</div>
                                  <div className={cx('name')}>{value['name']}</div>
                                  <div className={cx('cnt')}>{value['cnt']} solved</div>
                              </div>
                          </a>
                      )
                  })
                : data.map((value, i) => {
                      return (
                          <a href={`https://www.acmicpc.net/user/${value['name']}`} className={cx('a')} key={i}>
                              <div className={cx(i === 0 ? 'first' : i <= 3 ? 'second' : 'third', 'item')}>
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
