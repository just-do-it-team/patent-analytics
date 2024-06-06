import moment from 'moment';

export const USER_DATE_FORMAT = 'DD.MM.YYYY';
export const USER_DATE_TIME_FORMAT = 'DD.MM.YYYY HH:mm:ss';
export const USER_DATE_TIME_FORMAT_MIN = 'DD.MM.YYYY HH:mm';
export const USER_TIME_FORMAT = 'HH:mm';
export const DAY_MONTH_FORMAT = 'dddd, D MMMM';
export const DAY_MONTH_YEAR_FORMAT = 'D MMMM YYYY';
export const MONTH_FORMAT = 'D MMMM';
export const BACKEND_DATE_FORMAT = 'YYYY-MM-DD';

export function formatDateToString(date: string) {
    if (!date) {
        return '';
    }
    return moment(date).format(USER_DATE_FORMAT);
}

export function formatTimeToString(date: string) {
    return moment(date).format(USER_TIME_FORMAT);
}

export function formatDateToDayMonthType(date: string) {
    return moment(date).format(DAY_MONTH_FORMAT);
}

export function formatDateToMinFormat(date?: string) {
    if (!date) {
        return '';
    }
    return moment(date).format(USER_DATE_TIME_FORMAT_MIN);
}

export function formatDateWithTime(date?: string) {
    return moment(date).format(USER_DATE_TIME_FORMAT);
}

export function formatDateToBackend(date?: string) {
    return moment(date).format(BACKEND_DATE_FORMAT);
}
