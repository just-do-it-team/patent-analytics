import React, {
    FC, memo,
} from 'react';
import { Spin, SpinProps } from 'antd';
import { classNames } from '@/shared/lib/classNames/classNames';
import { SpinSize } from 'antd/lib/spin';
import classes from './spinner.module.scss';

export enum SpinnerType {
    LOCAL = 'local',
    GLOBAL = 'global',
}

interface SpinnerProps extends SpinProps {
    className?: string;
    size?: SpinSize;
    type?: SpinnerType;
}

export const Spinner: FC<SpinnerProps> = memo((props) => {
    const {
        className,
        size,
        type = SpinnerType.LOCAL,
    } = props;

    const mods: Record<string, boolean | undefined> = {
        [classes[type]]: true,
    };

    return (
        <Spin
            size={size}
            className={classNames(classes.Spinner, mods, [className])}
        />
    );
});
