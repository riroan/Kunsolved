import React, { useState, useEffect } from 'react'
import classnames from 'classnames/bind'
import styles from './navigation.module.scss'
import { getColor } from '../_config/color'
import MainCard from '../maincard/index'
import 'react-svg-radar-chart/build/css/index.css'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, RadialLinearScale, PointElement, LineElement, Filler } from 'chart.js'
import { Pie, Radar } from 'react-chartjs-2'
import URL from '../_config/config'

const cx = classnames.bind(styles)
ChartJS.register(ArcElement, Tooltip, Legend)
ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

export default function Navigation() {
    const [pieData, setPieData] = useState<number[]>([])
    const [tagData, setTagData] = useState<number[]>([])
    const tierLabels = ['unrated', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'ruby']
    const tagLabels = ['수학', '구현', '그리디', '문자열', '자료구조', '그래프', 'DP', '기하학']
    const backgroundcolor = tierLabels.map(label => getColor(label))
    const options = {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 1.7
    }

    useEffect(() => {
        var url = `${URL}/v1/level`
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                setPieData(Object.values(res))
            })
        url = `${URL}/v1/tag`
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                setTagData(Object.values(res))
            })
    }, [])

    return (
        <div className={cx('box')}>
            <MainCard
                className={cx('card')}
                title="건국대학교 레벨별 해결 문제 수"
                element={
                    <Pie
                        className={cx('chart')}
                        data={{
                            labels: tierLabels,
                            datasets: [
                                {
                                    data: pieData,
                                    backgroundColor: backgroundcolor,
                                    borderWidth: 0,
                                },
                            ],
                        }}
                        options={options}
                    />
                }
            />
            <MainCard
                className={cx('card')}
                title="건국대학교 주요 태그별 해결 문제 수"
                element={
                    <Radar
                        className={cx('chart')}
                        data={{
                            labels: tagLabels,
                            datasets: [
                                {
                                    label: '해결 수',
                                    data: tagData,
                                    backgroundColor: 'rgba(255,123,123,0.5)',
                                },
                            ],
                        }}
                        options={options}
                    />
                }
            />
        </div>
    )
}
