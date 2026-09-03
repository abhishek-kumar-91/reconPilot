import { Link } from "react-router-dom";
import { PageHeader } from "../components/ui/PageHeader";

export function NotFound() {
  return (
    <>
      <PageHeader title="404" description="The page you requested does not exist." />
      <Link className="button primary" to="/dashboard">Back to dashboard</Link>
    </>
  );
}