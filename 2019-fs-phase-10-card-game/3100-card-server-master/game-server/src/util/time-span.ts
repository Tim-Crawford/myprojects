/**
 * An interval of time stored in milliseconds.
 */
export class TimeSpan {
    /**
     * The total number of milliseconds.
     */
    public readonly totalMilliseconds: number;

    /**
     * The total number of seconds.
     */
    public get totalSeconds(): number {
        return this.totalMilliseconds / 1000;
    }

    /**
     * The total number of minutes.
     */
    public get totalMinutes(): number {
        return this.totalSeconds / 60;
    }

    /**
     * The total number of hours.
     */
    public get totalHours(): number {
        return this.totalMinutes / 60;
    }

    /**
     * The total number of days.
     */
    public get totalDays(): number {
        return this.totalHours / 24;
    }

    /**
     * An integer representing the seconds component of the interval in the range of [0, 60).
     */
    public get seconds(): number {
        return Math.floor(this.totalSeconds % 60);
    }

    /**
     * An integer representing the minutes component of the interval in the range of [0, 60).
     */
    public get minutes(): number {
        return Math.floor(this.totalMinutes % 60);
    }

    /**
     * An integer representing the hours component of the interval in the range of [0, 24).
     */
    public get hours(): number {
        return Math.floor(this.totalHours % 24);
    }

    /**
     * An integer representing the days component of the interval.
     */
    public get days(): number {
        return Math.floor(this.totalDays);
    }

    /**
     * Constructor.
     * @param days The number of days to add to this interval.
     * @param hours The number of hours to add to this interval.
     * @param minutes The number of minutes to add to this interval.
     * @param seconds The number of seconds to add to this interval.
     * @param milliseconds The number of milliseconds to add to this interval.
     */
    public constructor(days?: number, hours?: number, minutes?: number, seconds?: number, milliseconds?: number) {
        this.totalMilliseconds = 0;

        if (milliseconds !== undefined) {
            this.totalMilliseconds += milliseconds;
        }

        if (seconds !== undefined) {
            this.totalMilliseconds += seconds * 1000;
        }

        if (minutes !== undefined) {
            this.totalMilliseconds += minutes * 1000 * 60;
        }

        if (hours !== undefined) {
            this.totalMilliseconds += hours * 1000 * 60 * 60;
        }

        if (days !== undefined) {
            this.totalMilliseconds += days * 1000 * 60 * 60 * 24;
        }
    }
}