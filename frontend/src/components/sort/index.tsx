import React, { useState } from 'react'
import classnames from 'classnames/bind'
import styles from './sort.module.scss'
const cx = classnames.bind(styles)

type SortProps = {
    sortFunction: (flag: boolean, type: number) => void
}

export enum SortType {
    ID = 0,
    LEVEL = 1,
    TITLE = 2,
    RANDOM = 3,
}

export default function Sort({ sortFunction }: SortProps) {
    const [mode, setMode] = useState(0)
    const elements = ['번호', '레벨', '제목', '랜덤']
    return (
        <div className={cx('main')}>
            <div className={cx('title')}>정렬</div>
            {elements.map((value, ix) => (
                <button
                    key={ix}
                    className={cx(mode === ix && 'selected')}
                    onClick={() => {
                        sortFunction(mode === ix, ix)
                        setMode(ix)
                    }}
                >
                    {value}
                </button>
            ))}
        </div>
    )
}
