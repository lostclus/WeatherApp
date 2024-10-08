export type ServerErrors = { detail: { msg: string, loc: string[] }[] };
export type ErrorsDict = { [index: string]: string[]};

export class FormErrors {
  _errors: ErrorsDict = {};

  hasErrors(): boolean {
    return Object.keys(this._errors).length > 0;
  }

  hasErrorsIn(field: string): boolean {
    return field in this._errors;
  }

  getErrorsIn(field: string): string | null {
    if (!this.hasErrorsIn(field)) return null;
    return this._errors[field].join(" ");
  }

  addError(field: string, message: string): void {
    this._errors[field] = this._errors[field] || [];
    this._errors[field].push(message);
  }

  addFromServer(serverErrors: ServerErrors): void {
    serverErrors.detail.forEach(
      ({ msg, loc }) => {
	const field = loc.at(-1) as string;
	this.addError(field, msg);
      }
    );
  }
}
