import React, { useState, useEffect } from 'react'
import { PieChart } from 'react-minimal-pie-chart'
import color, { tier2color } from '../_config/color'
import styles from './chart.module.scss'
import classnames from 'classnames/bind'
import { DataEntry } from 'react-minimal-pie-chart/types/commonTypes'
const cx = classnames.bind(styles)

function Chart() {
    // TODO : data는 props로 받게 변경
    const [data, setData] = useState<DataEntry[]>([])

    useEffect(() => {
        const url = 'http://localhost:8000/byExp'
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
                for (var d in res) {
                    sum += res[d]
                }
                for (d in res) {
                    const title = d
                    const value = ((res[d] / sum) * 100) | 0
                    const tierColor = tier2color(parseInt(d), true)
                    pieData.push({ title: title, value: value, color: color[tierColor] })
                }
                setData(pieData)
            })
    }, [])

    return (
        <div>
            <PieChart className={cx('chart')} data={data} />
        </div>
    )
}

export default Chart
