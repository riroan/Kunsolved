import React, { useState, useEffect, ReactElement } from 'react'
import Chart from '../chart'
import classnames from 'classnames/bind'
import styles from './maingraph.module.scss'
import color, { tier2color } from '../_config/color'
import { DataEntry } from 'react-minimal-pie-chart/types/commonTypes'
const cx = classnames.bind(styles)

export default function MainGraph() {
    const [data, setData] = useState<DataEntry[]>([])
    const [count, setCount] = useState<ReactElement[]>([])

    useEffect(() => {
        const url = 'http://localhost:8000/byLevel'
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                var sum = 0
                var pieData = []
                var countData = []
                for (var d in res) {
                    sum += res[d]
                }
                for (d in res) {
                    const value = (res[d] / sum) * 100
                    const tierColor = tier2color(parseInt(d), false)
                    pieData.push({ title: tierColor, value: value, color: color[tierColor] })
                    countData.push(
                        <li style={{ display: 'flex', alignItems: 'center' }}>
                            <div style={{ width: '10px', height: '10px', background: color[tierColor], marginRight: '5px' }}></div>
                            {res[d]}
                        </li>
                    )
                }
                setCount(countData)
                setData(pieData)
            })
    }, [])
    return (
        <div className={cx('box')}>
            <div className={cx('title')}>건국대학교 티어별 해결한 문제 수</div>
            <div className={cx('body')}>
                <div className={cx('left')}>
                    <Chart data={data} />
                </div>
                <div className={cx('right')}>
                    <ul>{count}</ul>
                </div>
            </div>
        </div>
    )
}
