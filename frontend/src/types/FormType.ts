import { SubmitHandler } from "react-hook-form";

export type FormProps = {
  onSubmit: SubmitHandler<{ patentId: string; companyName: string }>;
};
