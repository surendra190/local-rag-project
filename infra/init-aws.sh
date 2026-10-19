#!/bin/sh

set -e

awslocal s3 mb s3://documents || true

echo "S3 bucket 'documents' ready"