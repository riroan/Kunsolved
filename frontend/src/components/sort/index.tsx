import React, { useState } from 'react'
import classnames from 'classnames/bind'
import styles from './sort.module.scss'
import { MdArrowDownward, MdArrowUpward, MdOutlineRefresh } from 'react-icons/md'
import { Checkbox, FormGroup, FormControlLabel } from '@mui/material'
const cx = classnames.bind(styles)

type SortProps = {
    sortFunction: (flag: boolean, type: number) => void
    handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void
    hide: boolean
}

export enum SortType {
    ID = 0,
    LEVEL = 1,
    TITLE = 2,
    RANDOM = 3,
}

export default function Sort({ sortFunction, handleChange, hide }: SortProps) {
    const [mode, setMode] = useState(0)
    const [arrow, setArrow] = useState(<MdArrowUpward />)
    const [arrowIx, setArrowIx] = useState(0)
    const [check, setCheck] = useState(false)
    const elements = ['번호', '레벨', '제목', '랜덤']
    return (
        <div className={cx('main')}>
            <div className={cx('container')}>
                <div className={cx('title')}>정렬</div>
                {elements.map((value, ix) => (
                    <button
                        key={ix}
                        className={cx(mode === ix && 'selected')}
                        onClick={() => {
                            if (ix === SortType.RANDOM) {
                                setArrow(<MdOutlineRefresh />)
                            } else if (mode === ix) {
                                setArrowIx(1 - arrowIx)
                                setArrow(arrowIx === 0 ? <MdArrowDownward /> : <MdArrowUpward />)
                            } else {
                                setArrowIx(0)
                                setArrow(<MdArrowUpward />)
                            }
                            sortFunction(mode === ix, ix)
                            setMode(ix)
                        }}
                    >
                        {value}
                        {mode === ix && arrow}
                    </button>
                ))}
            </div>
            {hide && (
                <FormGroup className={cx('group')}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={check}
                                onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                    setCheck(event.target.checked)
                                    handleChange(event)
                                }}
                                color="default"
                            />
                        }
                        label="티어숨기기"
                    />
                </FormGroup>
            )}
        </div>
    )
}

Sort.defaultProps = {
    hide: false,
    handleChange: () => {},
}
