import type { ServerErrors } from './types'

type ErrorsDict = {
    [index: string]: string[]
};

export class FormErrors {
  private _errors: ErrorsDict = {};

  catchAllField = "__all__"

  hasErrors(): boolean {
    return Object.keys(this._errors).length > 0;
  }

  hasErrorsIn(...fields: string[]): boolean {
    return fields.some((field) => field in this._errors);
  }

  getErrors(): string | null {
    return this.getErrorsIn(...Object.keys(this._errors));
  }

  getErrorsIn(...fields: string[]): string | null {
    const errors: string[] = [];

    fields.forEach((field) => {
      if (field in this._errors)
	errors.splice(-1, 0, ...this._errors[field]);
    });

    if (errors.length === 0) return null;
    return errors.join(" ");
  }

  addError(field: string, message: string): void {
    this._errors[field] = this._errors[field] || [];
    this._errors[field].push(message);
  }

  addFromServer(serverErrors: ServerErrors, ): void {
    if (typeof serverErrors.detail === "string") {
      this.addError(this.catchAllField, serverErrors.detail)
    } else {
      serverErrors.detail.forEach(
	({ msg, loc }) => {
	  const field = loc.at(-1) as string;
	  this.addError(field, msg);
	}
      );
    }
  }

  clear(): void {
    this._errors = {};
  }
}
